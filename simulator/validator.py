from typing import Dict, Any,List
class ValidationError(Exception):
    pass
def _ensure_type(field_name: str, value, expected_type):
    if not isinstance(value, expected_type):
        raise ValidationError(f"Field '{field_name}' must be of type {expected_type.__name__}")
def validate_automaton_schema(automaton: Dict[str, Any]) -> None:
    required_fields = ["id", "name", "initial_state", "acceptance_states", "alphabet", "states", "transitions"]
    for field in required_fields:
        if field not in automaton:
            raise ValidationError(f"Missing required field: {field}")
        if automaton[field] is None:
            raise ValidationError(f"Field '{field}' cannot be Null")
    _ensure_type("id", automaton["id"], str)
    _ensure_type("name", automaton["name"], str)
    _ensure_type("initial_state", automaton["initial_state"], str)
    _ensure_type("acceptance_states", automaton["acceptance_states"], List)
    _ensure_type("alphabet", automaton["alphabet"], List)
    _ensure_type("states", automaton["states"], List)
    _ensure_type("transitions", automaton["transitions"], list)
    states= automaton["states"]
    alphabet = automaton["alphabet"]
    initial= automaton["initial_state"]
    acceptance = automaton["acceptance_states"]
    transitions = automaton["transitions"]
    if initial not in states:
        raise ValidationError(f"Initial state '{initial}' is not defined list")

    for i in acceptance:
        if i not in states:
            raise ValidationError(f"Acceptance state '{i}' is not defined in states list")
    for i  in alphabet:
        if not isinstance(i, str):
            raise ValidationError(f"Alphabet symbol '{i}' must be a string")
        
    for i in transitions:
        if not isinstance(i, dict):
            raise ValidationError("Each transition must be a dictionary")
        for key in ["from_state", "symbol", "to_state"]:
            if key not in i:
                raise ValidationError(f"Transition is missing key: {key}")
            if i[key] is None:
                raise ValidationError(f"Transition  '{key}' value cannot be Null")
        if i["from_state"] not in states:
            raise ValidationError(f"Transition 'from_state' '{i['from_state']}' is not in the list of states")
        if i["to_state"] not in states:
            raise ValidationError(f"Transition 'to_state' '{i['to_state']}' is not in the list of states")
        if i["symbol"] not in alphabet:
            raise ValidationError(f"Transition symbol '{i['symbol']}' is not in the alphabet")
    mapping={s: set() for s in states}
    for i in transitions:
        mapping[i["from_state"]].add(i["symbol"])
    missing=[]
    for i in states:
        missing_symbols =[s for s in alphabet if s not in mapping.get(i, set())]
        if missing_symbols:
            missing.append((i, missing_symbols))
    if missing:
        details = ", ".join(f"State '{state}' is missing symbols:{m}" for state ,m in missing)
        raise ValidationError(f"Some states are missing symbols from the alphabet: {details}")
    return

