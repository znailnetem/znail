import unittest
from unittest.mock import call, patch

from znail.netem.tc import Tc
from znail.ui import app


class TestWhiteList(unittest.TestCase):
    def setUp(self):
        tc_clear_patcher = patch.object(Tc, "clear")
        self.tc_clear = tc_clear_patcher.start()
        self.addCleanup(tc_clear_patcher.stop)

        tc_apply_patcher = patch.object(Tc, "apply")
        self.tc_apply = tc_apply_patcher.start()
        self.addCleanup(tc_apply_patcher.stop)

        self.client = app.test_client()

    def tearDown(self):
        self.client.post("/api/whitelist/clear")

    def test_empty(self):
        response = self.client.get("/api/whitelist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_can_be_set(self):
        response = self.client.post("/api/whitelist", json=[{"ip_address": "1.2.3.4"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        response = self.client.get("/api/whitelist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"ip_address": "1.2.3.4"}])

    def test_multiple_entries(self):
        response = self.client.post("/api/whitelist", json=[{"ip_address": "1.2.3.4"}, {"ip_address": "2.3.4.5"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        response = self.client.get("/api/whitelist")
        self.assertEqual(response.status_code, 200)
        self.assertIn({"ip_address": "1.2.3.4"}, response.json)
        self.assertIn({"ip_address": "2.3.4.5"}, response.json)

    def test_can_not_be_set_to_invalid_value(self):
        response = self.client.post("/api/whitelist", json={"invalid": "data"})
        self.assertEqual(response.status_code, 422)

    def test_bad_request(self):
        response = self.client.post("/api/whitelist")
        self.assertEqual(response.status_code, 400)

    def test_can_be_cleared(self):
        response = self.client.post("/api/whitelist/clear")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        last_call = self.tc_apply.call_args_list[-1]
        self.assertEqual(last_call, call({}))
