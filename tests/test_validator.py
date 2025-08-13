import unittest
from simulator.validator import validate_automaton_schema, ValidationError

class ValidatorTests(unittest.TestCase):

    def setUp(self):
        self.base_automaton = {
            "id": "a1",
            "name": "Test Automaton",
            "initial_state": "q0",
            "acceptance_states": ["q0"],
            "alphabet": ["0", "1"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "0", "to_state": "q0"},
                {"from_state": "q0", "symbol": "1", "to_state": "q1"},
                {"from_state": "q1", "symbol": "0", "to_state": "q0"},
                {"from_state": "q1", "symbol": "1", "to_state": "q1"}
            ]
        }

    def test_valid_automaton_passes(self):
        validate_automaton_schema(self.base_automaton)

    def test_invalid_initial_state(self):
        bad_auto = dict(self.base_automaton)
        bad_auto["initial_state"] = "qX"
        with self.assertRaises(ValidationError):
            validate_automaton_schema(bad_auto)

    def test_invalid_acceptance_state(self):
        bad_auto = dict(self.base_automaton)
        bad_auto["acceptance_states"] = ["qX"]
        with self.assertRaises(ValidationError):
            validate_automaton_schema(bad_auto)

    def test_symbol_not_in_alphabet(self):
        bad_auto = dict(self.base_automaton)
        bad_auto["transitions"][0]["symbol"] = "2"
        with self.assertRaises(ValidationError):
            validate_automaton_schema(bad_auto)

    def test_missing_transition(self):
        bad_auto = dict(self.base_automaton)
        bad_auto["transitions"] = [
            {"from_state": "q0", "symbol": "0", "to_state": "q0"}
        ]
        with self.assertRaises(ValidationError):
            validate_automaton_schema(bad_auto)
