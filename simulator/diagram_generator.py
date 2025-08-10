import os 
from graphviz import Digraph
from typing import Optional
from simulator.automaton import Automaton

class DiagramGenerator:
    def __init__(self, output_dir: str = 'generated_diagram'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, automaton: Automaton, filename_without_ext:str) ->str:
        dot = Digraph(format='png')
        dot.attr(rankdir='LR', size='8,5')
        dot.node("",shape="none")
        