import unittest
import requests
import json

url = "http://localhost:8080/football"

def fetch(url, data):
    return requests.post(url, data=data)


class TestValidRequest(unittest.TestCase):

    def setUp(self):
        self.resp = fetch(url, data=json.dumps({"game_id": "qwertyui", "home_expected": 2.1, "away_expected": 1.1}))

    def test_statusCode(self):
        self.assertEqual(self.resp.status_code, 200)


class TestInValidRequest_BadJson(unittest.TestCase):

    def setUp(self):
        self.resp = fetch(url, data='{"game_id": "qwertyui", "home_expected": 2.1, "away_expected": 1.1)')

    def test_statusCode(self):
        self.assertEqual(self.resp.status_code, 400)


class TestInValidRequest_BadRequest(unittest.TestCase):

    def setUp(self):
        self.resp = fetch(url,  data=json.dumps({"game_id": "qwertyui", "home_exp": 2.1, "away_exp": 1.1}))

    def test_statusCode(self):
        self.assertEqual(self.resp.status_code, 400)