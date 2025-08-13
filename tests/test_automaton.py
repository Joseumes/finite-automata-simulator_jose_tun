import unittest
from simulator.automaton import Automaton

class AutomatonTests(unittest.TestCase):

    def setUp(self):
        data = {
            "id": "a1",
            "name": "Binary strings ending in 1",
            "initial_state": "q0",
            "acceptance_states": ["q1"],
            "alphabet": ["0", "1"],
            "states": ["q0", "q1"],
            "transitions": [
                {"from_state": "q0", "symbol": "0", "to_state": "q0"},
                {"from_state": "q0", "symbol": "1", "to_state": "q1"},
                {"from_state": "q1", "symbol": "0", "to_state": "q0"},
                {"from_state": "q1", "symbol": "1", "to_state": "q1"}
            ]
        }
        self.automaton = Automaton.from_dict(data)

    def test_accepts_strings_ending_in_1(self):
        self.assertTrue(self.automaton.process_input("1"))
        self.assertTrue(self.automaton.process_input("101"))
        self.assertTrue(self.automaton.process_input("111"))

    def test_rejects_strings_not_ending_in_1(self):
        self.assertFalse(self.automaton.process_input("0"))
        self.assertFalse(self.automaton.process_input("10"))
        self.assertFalse(self.automaton.process_input(""))
