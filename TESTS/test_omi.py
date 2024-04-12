import unittest
import requests
from flask import Flask
import time

app = Flask(__name__)

class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://192.168.56.102:5000'  # Replace with your app's URL
        # Start your Flask app in a separate process or thread here

    def _send_request_with_retry(self, method, url, retries=3, timeout=5, **kwargs):
        for _ in range(retries):
            try:
                response = requests.request(method, url, timeout=timeout, **kwargs)
                response.raise_for_status()  # Raise an exception for non-successful status codes
                return response
            except requests.exceptions.RequestException as e:
                #print(f"Failed to send request: {e}")
                time.sleep(1)  # Delay between retries
        raise unittest.TestCase.failureException(f"Failed to send request after {retries} retries")

    def test_server_status(self):
        url = f'{self.base_url}/'
        response = self._send_request_with_retry('GET', url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Server is running')  # Replace with your server response text

    def test_generate_osm(self):
        url = f'{self.base_url}/generate_osm'
        payload = {
            "message_id": 123,
            "message_text": "Sample message",
            "device_id": "ABC123",
            "expiry": "2023-06-30"
        }
        response = self._send_request_with_retry('POST', url, json=payload)
        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.text, 'Message saved successfully')  # Replace with the expected response text

    def test_add_entitlement(self):
        url = f'{self.base_url}/addentitlement'
        payload = {
            "device_id": 7010000000,
            "package_ids": "2",
            "expiry": "2023-06-30"
        }
        response = self._send_request_with_retry('POST', url, json=payload)
        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.text, 'Entitlements added successfully')  # Replace with the expected response text

    def test_device_keys(self):
        url = f'{self.base_url}/device_keys'
        payload = {
            "device_id": 7010000000,
            "bskeys": "701000000009876",
            "expiry": "2023-06-30"
        }
        response = self._send_request_with_retry('POST', url, json=payload)
        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.text, 'Devices added successfully')  # Replace with the expected response text

if __name__ == '__main__':
    unittest.main()
