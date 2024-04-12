import unittest
import importlib.util

spec = importlib.util.spec_from_file_location('omi', r'/root/mycas/mycas-CICD/SMS-CAS/omi.py')
omi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(omi)

app = omi.app
class FlaskServerTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client

    def test_server_status(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Server is running')  # Replace with your server response text

    def test_generateosm(self):
        payload = {
            "message_id": 123,
            "message_text": "Sample message",
            "device_id": "ABC123",
            "expiry": "2023-06-30"
        }
        response = self.app.post('/generate_osm', json=payload)

        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.data.decode('utf-8'), 'Message saved successfully')  # Replace with the expected response text

    def test_addentitlement(self):
        payload = {
            "device_id": 7010000000,
            "package_ids": "2",
            "expiry": "2023-06-30"
        }
        response = self.app.post('/addentitlement', json=payload)

        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.data.decode('utf-8'), 'Entitlements added successfully')  # Replace with the expected response text

    def test_device_keys(self):
        payload = {
            "device_id": 7010000000,
            "bskeys": "701000000009876",
            "expiry": "2023-06-30"
        }
        response = self.app.post('/device_keys', json=payload)

        self.assertEqual(response.status_code, 200)  # Replace with the expected status code
        self.assertEqual(response.data.decode('utf-8'), 'Devices added successfully')  # Replace with the expected response text

if __name__ == '__main__':
    unittest.main()


