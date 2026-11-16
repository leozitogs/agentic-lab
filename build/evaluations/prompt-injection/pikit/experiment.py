"""Identidade experimental, diário completo e publicação serializada."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
from urllib.parse import urlsplit
import uuid


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(f"Execução em uso: {path}. Após confirmar que o processo terminou, "
                           "remova a trava remanescente e tente novamente.") from None
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        path.unlink()


def manifest(args, kit: Path, inbox: dict, tasks: list, attacks: list,
             configs: dict, max_turns: int, version: str) -> dict:
    endpoint = args.host if args.provider == "ollama" else args.base_url
    parsed = urlsplit(endpoint)
    if (parsed.scheme not in ("http", "https") or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment):
        raise ValueError("Endpoint deve usar HTTP(S), sem credenciais, query ou fragmento.")
    sources = [kit / "run_eval.py", *sorted((kit / "pikit").glob("*.py"))]
    identity = {
        "schema_version": 1, "kit_version": version,
        "sources": {p.relative_to(kit).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sources},
        "data": {"inbox": inbox, "tasks": tasks, "attacks": attacks},
        "configurations": {name: asdict(value[1]) for name, value in configs.items()},
        "provider": args.provider, "endpoint": endpoint.rstrip("/"), "model": args.model,
        "model_revision": args.model_revision, "temperature": args.temperature,
        "max_turns": max_turns, "python": platform.python_version(),
        "seed_policy": "rep-index",
    }
    if args.fresh or not args.model_revision:
        identity["invocation"] = uuid.uuid4().hex
    try:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=kit,
                                           stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    return {"experiment_id": hashlib.sha256(canonical(identity)).hexdigest(),
            "identity": identity, "git_revision": revision}


def load_journal(path: Path, experiment: dict) -> dict[tuple, dict]:
    if not path.exists():
        return {}
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    offset = 0
    done = {}
    identity = experiment["experiment_id"]
    spec = experiment["identity"]
    task_ids = {t["id"] for t in spec["data"]["tasks"]}
    attack_ids = {a["id"] for a in spec["data"]["attacks"]}
    for index, line in enumerate(lines):
        try:
            row = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            if index != len(lines) - 1 or line.endswith(b"\n"):
                raise ValueError(f"Diário corrompido na linha {index + 1}: {path}") from None
            atomic_write(path.with_name(f"interrupted-{uuid.uuid4().hex}.bin"), line)
            atomic_write(path, data[:offset])
            break
        if (not isinstance(row, dict) or row.get("experiment_id") != identity
                or row.get("config") not in spec["configurations"]
                or row.get("task") not in task_ids
                or (row.get("attack") is not None and row["attack"] not in attack_ids)
                or type(row.get("rep")) is not int or row["rep"] < 0
                or not {"error", "hit_turn_limit", "final_answer", "tools",
                        "utility", "attack_success", "seconds"}.issubset(row)):
            raise ValueError(f"Registro incompatível na linha {index + 1}: {path}")
        done[(row["config"], row["task"], row["attack"], row["rep"])] = row
        offset += len(line)
    else:
        if data and not data.endswith(b"\n"):
            atomic_write(path, data + b"\n")
    return done


def append_record(stream, row: dict) -> None:
    stream.write(canonical(row) + b"\n")
    stream.flush()
    os.fsync(stream.fileno())


def publish(results_dir: Path, results: dict, experiment: dict, journal: bytes,
            render, notes: dict) -> None:
    publication = uuid.uuid4().hex
    identity = experiment["experiment_id"]
    relative = Path("experiments") / identity / publication
    results["experiment_id"] = identity
    results["publication_id"] = publication
    results["audit_artifacts"] = relative.as_posix()
    publication_manifest = {**experiment, "publication_id": publication}
    json_bytes = canonical(results) + b"\n"
    report_bytes = render(results, notes).replace("\n", os.linesep).encode("utf-8")
    with exclusive_lock(results_dir / ".publish.lock"):
        archive = results_dir / relative
        atomic_write(archive / "manifest.json", canonical(publication_manifest) + b"\n")
        atomic_write(archive / "runs.jsonl", journal)
        atomic_write(archive / "results.json", json_bytes)
        atomic_write(archive / "report.md", report_bytes)
        atomic_write(results_dir / "results.json", json_bytes)
        atomic_write(results_dir / "report.md", report_bytes)


def regenerate(results_dir: Path, render, notes: dict) -> None:
    with exclusive_lock(results_dir / ".publish.lock"):
        results = json.loads((results_dir / "results.json").read_text(encoding="utf-8"))
        atomic_write(results_dir / "report.md", render(results, notes).replace("\n", os.linesep).encode("utf-8"))
