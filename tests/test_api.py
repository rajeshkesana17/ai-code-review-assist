import unittest
from unittest.mock import patch

from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_empty_code_returns_400(self):
        response = self.client.post('/api/analyze', json={'code': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], 'No code provided.')

    def test_oversized_code_returns_413(self):
        response = self.client.post('/api/analyze', json={'code': 'x' * 30001})
        self.assertEqual(response.status_code, 413)

    @patch('app.gemini_service.analyze_code')
    def test_language_and_explanation_language_are_forwarded(self, analyze_code):
        analyze_code.return_value = {
            'overall_score': 90,
            'summary': 'Looks good',
            'issues': [],
            'refactored_code': 'print(1)',
            'language': 'Python',
            'explanation_language': 'Telugu',
        }
        response = self.client.post(
            '/api/analyze',
            json={
                'code': 'print(1)',
                'language': 'Python',
                'explanation_language': 'Telugu',
            },
        )
        self.assertEqual(response.status_code, 200)
        analyze_code.assert_called_once_with('print(1)', 'Python', 'Telugu')
        self.assertEqual(response.get_json()['explanation_language'], 'Telugu')


if __name__ == '__main__':
    unittest.main()
