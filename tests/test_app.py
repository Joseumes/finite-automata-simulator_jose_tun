import json
import os
import unittest
from api.app import app

class AutomataAPITests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_process_automata_from_json_file(self):
        """Test sending JSON file"""
        json_path = os.path.join("examples", "sample_automata.json")
        with open(json_path, "rb") as f:
            response = self.app.post(
                "/process_automaton",
                data={"file": (f, "sample_automata.json")},
                content_type="multipart/form-data"
            )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)

        for item in data:
            self.assertIn("id", item)
            self.assertIn("suscess", item)
            self.assertIsInstance(item["suscess"], bool)

    def test_process_automata_from_json_body(self):
        """Test sending JSON in request body"""
        json_path = os.path.join("examples", "sample_automata.json")
        with open(json_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        response = self.app.post(
            "/process_automaton",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
