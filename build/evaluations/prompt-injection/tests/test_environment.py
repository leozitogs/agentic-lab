"""Caixa fictícia, ferramentas simuladas e injeção nos vetores."""
import json
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pikit.environment import Mailbox, ToolLog, build_inbox, load_all, plant  # noqa: E402

INBOX, TASKS, ATTACKS = load_all()
ATTACK = {a["id"]: a for a in ATTACKS}
TASK = {t["id"]: t for t in TASKS}


class Data(unittest.TestCase):
    def test_everything_is_fictional(self):
        """Todo endereço e domínio usa .example (RFC 2606): nada de dado real."""
        blob = json.dumps([INBOX, TASKS, ATTACKS], ensure_ascii=False)
        for addr in re.findall(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)", blob):
            self.assertTrue(addr.endswith(".example"), addr)
        for host in re.findall(r"https?://([\w-]+(?:\.[\w-]+)+)", blob):
            self.assertTrue(host.endswith(".example"), host)

    def test_targets_and_goals_are_consistent(self):
        ids = {e["id"] for e in INBOX["emails"]}
        for t in TASKS:
            self.assertIn(t["injection_target"], ids)
            self.assertEqual(INBOX["user"]["today"],
                             next(e["date"] for e in INBOX["emails"] if e["id"] == t["injection_target"]))
        for a in ATTACKS:
            self.assertIn(a["goal"]["type"], {"send_to", "leak_secret", "inject_url"})
            if a["goal"]["type"] == "send_to":
                self.assertIn(a["goal"]["address"], a["payload"])
            if a["goal"]["type"] == "inject_url":
                self.assertIn(a["goal"]["domain"], a["payload"])
                self.assertNotIn(a["goal"]["domain"], INBOX["allowed_link_domains"])

    def test_secret_only_in_profile(self):
        secret = INBOX["user"]["secret"]
        self.assertNotIn(secret, json.dumps(INBOX["emails"] + ATTACKS + TASKS, ensure_ascii=False))

    def test_six_vectors(self):
        self.assertEqual({a["vector"] for a in ATTACKS},
                         {"instrucao_no_corpo", "comentario_html", "assinatura", "anexo_texto",
                          "urgencia_falsa", "falso_sistema"})


class Planting(unittest.TestCase):
    EMAIL = next(e for e in INBOX["emails"] if e["id"] == "e01")

    def test_append_and_prepend(self):
        self.assertTrue(plant(self.EMAIL, ATTACK["A1"])["body"].endswith(ATTACK["A1"]["payload"]))
        self.assertTrue(plant(self.EMAIL, ATTACK["A5"])["body"].startswith(ATTACK["A5"]["payload"]))

    def test_html_comment(self):
        body = plant(self.EMAIL, ATTACK["A2"])["body"]
        self.assertTrue(body.startswith("<html><body><p>"))
        self.assertIn(f"<!-- {ATTACK['A2']['payload']} --></body>", body)

    def test_signature(self):
        self.assertIn("\n--\n" + ATTACK["A3"]["payload"], plant(self.EMAIL, ATTACK["A3"])["body"])

    def test_attachment(self):
        planted = plant(self.EMAIL, ATTACK["A4"])
        self.assertEqual(planted["body"], self.EMAIL["body"])
        self.assertEqual(planted["attachments"][-1], {"name": "leia-me.txt", "text": ATTACK["A4"]["payload"]})

    def test_build_inbox_touches_only_target_and_copies(self):
        case = build_inbox(INBOX, TASK["T3"], ATTACK["A1"])
        changed = [e["id"] for e, o in zip(case["emails"], INBOX["emails"]) if e != o]
        self.assertEqual(changed, ["e02"])
        self.assertNotIn(ATTACK["A1"]["payload"], json.dumps(INBOX, ensure_ascii=False))
        self.assertEqual(build_inbox(INBOX, TASK["T3"], None), INBOX)


class Tools(unittest.TestCase):
    def setUp(self):
        self.log = ToolLog()
        self.box = Mailbox(INBOX, self.log)

    def test_list_today(self):
        rows = json.loads(self.box.list_emails(date="today"))
        self.assertEqual([r["id"] for r in rows], ["e01", "e02", "e03", "e04", "e05"])
        self.assertEqual(len(json.loads(self.box.list_emails())), 8)
        self.assertEqual(len(json.loads(self.box.list_emails(date="11/11"))), 1)
        self.assertNotIn("body", rows[0])

    def test_read_email(self):
        data = json.loads(self.box.read_email("e03"))
        self.assertEqual(data["attachments"][0]["name"], "fatura-2231.txt")
        self.assertIn("erro", json.loads(self.box.read_email("e99")))
        self.assertEqual(self.log.events[-1].status, "erro")

    def test_send_is_simulated_and_logged(self):
        out = self.box.send_email(to="Ana <ana.souza@lumen.example>", subject="Oi", body="Teste")
        self.assertIn("simulado", out)
        self.assertEqual(self.log.sent(), [{"to": ["ana.souza@lumen.example"], "subject": "Oi", "body": "Teste"}])

    def test_send_without_recipient(self):
        self.box.send_email(to="", subject="x", body="y")
        self.assertEqual(self.log.sent(), [])
        self.assertEqual(self.log.events[-1].status, "erro")

    def test_contacts(self):
        self.assertEqual(len(json.loads(self.box.search_contacts("Ana"))), 2)
        self.assertEqual(self.box.best_contact("Ana"), ("", "ambíguo"))
        self.assertEqual(self.box.best_contact("Ana financeiro")[0], "ana.souza@lumen.example")
        self.assertEqual(self.box.best_contact("Rafael")[0], "rafael@estudionorte.example")
        self.assertEqual(self.box.best_contact("ninguém")[0], "")

    def test_unknown_tool_and_bad_args(self):
        self.assertIn("não existe", self.box.call("delete_all", {}))
        self.assertIn("erro", self.box.call("read_email", {"foo": 1}))
        self.assertIn("Erro", self.box.call("send_email", {"para": "x"}))
