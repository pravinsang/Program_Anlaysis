import ast
import networkx as nx
import matplotlib.pyplot as plt

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.graph.add_node(node.name)
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.graph.add_edge(self.current_function, node.func.id)
        self.generic_visit(node)

def generate_call_graph(source_code):
    tree = ast.parse(source_code)
    visitor = CallGraphVisitor()
    visitor.visit(tree)
    return visitor.graph

source_code = """
def function_a():
    function_b()
    function_c()

def function_b():
    function_d()

def function_c():
    pass

def function_d():
    function_e()

def function_e():
    pass

if __name__ == "__main__":
    function_a()
"""

call_graph = generate_call_graph(source_code)

# Draw the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(call_graph)
nx.draw(call_graph, pos, with_labels=True, arrows=True)
plt.show()
