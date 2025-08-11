import os
import time
import json
from flask import request, jsonify,current_app
from . import create_app
from simulator.validator import validate_automaton_schema,ValidationError
from simulator.automaton import Automaton
from simulator.diagram_generator import DiagramGenerator



app= create_app()

@app.route('/process_automaton', methods=['POST'])

def process_automaton():
    try:
        if 'file' in request.files:
            file = request.files['file']
            content = file.read()
            automata_list = json.loads(content)
        else:
            automata_list = request.get_json()
            if automata_list is None:
                return jsonify({"error": "Invalid JSON "}),400
        if not isinstance(automata_list, list):
            return jsonify({"error": "Top level must be list of automata"}),400
        results = []
        gen_dir = current_app.config.get('GENERATE_DIR', 'generated_diagram')
        os.makedirs(gen_dir, exist_ok=True)
        diagram_generator = DiagramGenerator(output_dir=gen_dir)
        for automaton_json in automata_list:
            automaton_id = automaton_json.get('id', "<unknown>")
            try:
                validate_automaton_schema(automaton_json)
                automaton = Automaton.from_dict(automaton_json)
                timestamp = int(time.time())
                diagram_path = diagram_generator.generate(automaton,f"automaton_{automaton_id}_{timestamp}")
                test_strings = automaton_json.get('test_strings', [])
                imputs_validation=[]
                for i in test_strings:
                    result=automaton.process_input(i)
                    imputs_validation.append({
                        "input": i,
                        "result": result
                    })
                results.append({
                    "id": automaton_id,
                    "suscess": True,
                    "diagram": diagram_path,
                    "inputs_validation": imputs_validation
                })
            except ValidationError as ve:
                results.append({
                    "id": automaton_id,
                    "suscess": False,
                    "error_description": str(ve)
                })
            except Exception as e:
                results.append({
                    "id": automaton_id,
                    "suscess": False,
                    "error": f"processing error: {str(e)} "
                })
        return jsonify(results), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file or body"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)