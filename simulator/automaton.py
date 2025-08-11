from typing import Dict, List, Tuple
from dataclasses import dataclass, field

@dataclass
class Automaton:
    id:str
    name: str
    initial_state: str
    acceptance_states: List[str]
    alphabet: List[str]
    states: List[str]
    transitions: Dict[Tuple[str, str], str] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict):
        trans_map = {}
        for i in data.get('transitions', []):
            key= (i["from_state"],i["symbol"])
            trans_map[key] = i["to_state"]
        return cls(
            id=data["id"],
            name=data["name"],
            initial_state=data["initial_state"],
            acceptance_states=data["acceptance_states"],
            alphabet=data["alphabet"],
            states=data["states"],
            transitions=trans_map
            )
    def process_input(self, input_string: str) -> bool:
        current = self.initial_state
        if input_string is None:
            input_string = ""
        for i in input_string:
            Key = (current, i)
            if Key not in self.transitions:
                return False
            current = self.transitions[Key]
        return current in self.acceptance_states
