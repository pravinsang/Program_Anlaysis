import os
from PyCG import CallGraphGenerator

def generate_call_graph(source_file, package):
    cg = CallGraphGenerator(source_file, package)
    cg.analyze()
    cg_output = cg.output()
    
    with open("call_graph.json", "w") as f:
        f.write(cg_output)

if __name__ == "__main__":
    source_file = "sample.py"
    package = "Program_Analyis"
    generate_call_graph(source_file, package)