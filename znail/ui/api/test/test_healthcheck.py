import unittest
from unittest.mock import patch

from znail.ui import app


class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        perform_health_check_patcher = patch("znail.ui.api.healthcheck.perform_health_checks")
        self.perform_health_check = perform_health_check_patcher.start()
        self.addCleanup(perform_health_check_patcher.stop)

        self.client = app.test_client()

    def test_perform_health_check(self):
        self.perform_health_check.return_value = {"Health check name": True}

        response = self.client.get("/api/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Health check name": True})
