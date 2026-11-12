"""Extração segura e hash do corpus, com um tarball sintético em memória (sem rede)."""
import io
import pathlib
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from ragkit import corpus  # noqa: E402

P = corpus.ARCHIVE_PREFIX


def make_tar(members: dict[str, bytes], symlink: str | None = None) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
        if symlink:
            info = tarfile.TarInfo(symlink)
            info.type = tarfile.SYMTYPE
            info.linkname = "/etc/passwd"
            tar.addfile(info)
    return buf.getvalue()


class Extract(unittest.TestCase):
    def test_only_regular_markdown_under_docs_is_read(self):
        archive = make_tar({
            f"{P}index.md": b"# Home\r\n\r\nText.\r\n",
            f"{P}user-guide/cli.md": b"# CLI\n",
            f"{P}img/logo.png": b"\x89PNG",
            f"{P}hooks.py": b"print('never executed')",
            "mkdocs-1.6.1/README.md": b"# outside docs",
            f"{P}../escape.md": b"# traversal",
        }, symlink=f"{P}link.md")
        docs = corpus.extract_docs(archive)
        self.assertEqual(sorted(docs), ["index.md", "user-guide/cli.md"])
        self.assertEqual(docs["index.md"], "# Home\n\nText.\n")  # CRLF normalizado

    def test_safe_rel(self):
        self.assertEqual(corpus._safe_rel(f"{P}a/b.md"), "a/b.md")
        for bad in (f"{P}../x.md", f"{P}a/../../x.md", "other/docs/x.md", f"{P}x.txt", f"{P}c:x.md"):
            self.assertIsNone(corpus._safe_rel(bad), bad)


class Manifest(unittest.TestCase):
    def test_hash_is_stable_and_order_independent(self):
        a = {"a.md": "one", "b.md": "two"}
        b = {"b.md": "two", "a.md": "one"}
        self.assertEqual(corpus.docs_manifest_sha256(a), corpus.docs_manifest_sha256(b))
        self.assertNotEqual(corpus.docs_manifest_sha256(a), corpus.docs_manifest_sha256({"a.md": "one!", "b.md": "two"}))
        self.assertNotEqual(corpus.docs_manifest_sha256(a), corpus.docs_manifest_sha256({"c.md": "one", "b.md": "two"}))

    def test_write_and_load_round_trip(self):
        docs = {"index.md": "# Home\n", "sub/page.md": "# Page\n"}
        with tempfile.TemporaryDirectory() as tmp:
            corpus.write_docs(docs, pathlib.Path(tmp))
            self.assertEqual(corpus.load_docs(pathlib.Path(tmp)), docs)

    def test_fetch_rejects_content_that_does_not_match(self):
        archive = make_tar({f"{P}index.md": b"# tampered\n"})
        with tempfile.TemporaryDirectory() as tmp:
            cache = pathlib.Path(tmp)
            (cache / corpus.ARCHIVE_NAME).write_bytes(archive)  # cache local, sem rede
            with self.assertRaises(corpus.CorpusError):
                corpus.fetch(cache)
            self.assertFalse((cache / f"mkdocs-{corpus.TAG}").exists())


if __name__ == "__main__":
    unittest.main()
