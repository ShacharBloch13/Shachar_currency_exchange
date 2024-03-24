import unittest
from unittest.mock import patch
from flask import Flask
from app.routes import init_app

class TestCurrencyConversion(unittest.TestCase):
    def setUp(self):
        """Set up test application client."""
        self.app = Flask(__name__)
        init_app(self.app)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('requests.get')
    def test_successful_conversion(self, mock_get):
        # Mock a successful API response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "conversion_rates": {
                "EUR": 0.85,
                "JPY": 110.0
            }
        }

        response = self.client.get('/currency/check?sum=100&baseCurrency=USD')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("EUR", data)
        self.assertAlmostEqual(data["EUR"], 85.0)

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        # Mock a failure scenario
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        response = self.client.get('/currency/check?sum=100&baseCurrency=USD')
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

    # Additional tests for exception handling and parameter validation can be added here.

if __name__ == '__main__':
    unittest.main()
