import unittest
from main import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_calculate_page(self):
        data = {
            'amount': '5000',
            'rate': '5',
            'time': '2'
        }
        response = self.app.post('/calculate', data=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_with_invalid_data(self):
        data = {
            'amount': 'invalid',
            'rate': '5',
            'time': '2'
        }
        response = self.app.post('/calculate', data=data)
        self.assertEqual(response.status_code, 400)  # должен вернуться код ошибки 400
        self.assertIn(b'Invalid input', response.data)


if __name__ == '__main__':
    unittest.main()