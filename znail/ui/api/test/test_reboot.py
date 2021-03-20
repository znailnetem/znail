import unittest
from unittest.mock import patch

from znail.ui import app


class TestReboot(unittest.TestCase):
    def setUp(self):
        reboot_patcher = patch("znail.ui.api.reboot.reboot")
        self.reboot_patcher = reboot_patcher.start()
        self.addCleanup(reboot_patcher.stop)

        self.client = app.test_client()

    def test_reboot(self):
        response = self.client.get("/api/reboot")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers["Location"], "http://localhost/")
        self.assertEqual(response.json, {"message": "ok"})
