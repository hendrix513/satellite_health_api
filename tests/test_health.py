import unittest
from unittest.mock import patch

import pandas as pd

from app import create_app

app = create_app()


class HealthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.data_history', pd.DataFrame({"time": [0, 1], "altitude": [100, 101]}))
    @patch('app._get_current_timestamp', return_value=100)
    def test_health_endpoint_all_data_out_of_range(self, mock_get_current_timestamp):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "No data available")

    @patch('app.data_history', pd.DataFrame({"time": [], "altitude": []}))
    def test_health_endpoint_no_data(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "No data available")

    @patch('app.data_history', pd.DataFrame({"time": [0, 1, 2, 3], "altitude": [300, 200, 160, 119]}))
    @patch('app._get_current_timestamp', return_value=60)
    def test_health_endpoint_warning(self, mock_get_current_timestamp):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "WARNING: RAPID ORBITAL DECAY IMMINENT")

    @patch('app.data_history', pd.DataFrame({"time": [0, 1, 2, 3], "altitude": [300, 200, 160, 120]}))
    @patch('app._get_current_timestamp', return_value=60)
    def test_health_endpoint_low(self, mock_get_current_timestamp):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Sustained Low Earth Orbit Resumed")

    @patch('app.data_history', pd.DataFrame({"time": [0, 1, 2, 3], "altitude": [300, 400, 160, 120]}))
    @patch('app._get_current_timestamp', return_value=60)
    def test_health_endpoint_ok(self, mock_get_current_timestamp):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Altitude is A-OK")
