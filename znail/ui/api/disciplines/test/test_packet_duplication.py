import unittest
from unittest.mock import patch

from znail.ui import app


class TestPacketCorruption(unittest.TestCase):

    def setUp(self):
        run_in_shell_patcher = patch('znail.netem.tc.run_in_shell')
        self.run_in_shell = run_in_shell_patcher.start()
        self.addCleanup(run_in_shell_patcher.stop)
        self.client = app.test_client()

    def tearDown(self):
        self.client.post('/api/disciplines/packet_duplication/clear')

    def test_empty(self):
        response = self.client.get('/api/disciplines/packet_duplication')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'percent': None})

    def test_can_be_set(self):
        response = self.client.post('/api/disciplines/packet_duplication', json={'percent': 1.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'ok'})

        response = self.client.get('/api/disciplines/packet_duplication')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'percent': 1.0})

    def test_can_be_updated(self):
        response = self.client.post('/api/disciplines/packet_duplication', json={'percent': 1.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'ok'})

        response = self.client.get('/api/disciplines/packet_duplication')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'percent': 1.0})

        response = self.client.post('/api/disciplines/packet_duplication', json={'percent': 2.0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'ok'})

        response = self.client.get('/api/disciplines/packet_duplication')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'percent': 2.0})

    def test_can_not_be_set_to_invalid_value(self):
        response = self.client.post('/api/disciplines/packet_duplication', json={'invalid': 'data'})
        self.assertEqual(response.status_code, 422)

    def test_can_be_cleared(self):
        response = self.client.post('/api/disciplines/packet_duplication/clear')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'ok'})
