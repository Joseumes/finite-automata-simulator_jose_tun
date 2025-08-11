import os 
from graphviz import Digraph
from typing import Optional
from simulator.automaton import Automaton

class DiagramGenerator:
    def __init__(self, output_dir: str = 'generated_diagrams'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, automaton: Automaton, filename_without_ext:str) ->str:
        dot = Digraph(format='png')
        dot.attr(rankdir='LR', size='8,5')
        dot.node("",shape="none")
        for state in automaton.states:
            if state in automaton.acceptance_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')
        dot.edge("", automaton.initial_state)
        edge_map={}
        for (from_state, symbol), to_state in automaton.transitions.items():
            key=(from_state, to_state)
            edge_map.setdefault(key, []).append(symbol)
        for (from_state, to_state), symbols in edge_map.items():
            label=",".join(symbols)
            dot.edge(from_state, to_state, label=label)
        output_path = os.path.join(self.output_dir, f"{filename_without_ext}.png")
        render_path_without_ext = os.path.join(self.output_dir, filename_without_ext)
        dot.render(render_path_without_ext, cleanup=True)
        return output_path 