import ast
import networkx as nx
import matplotlib.pyplot as plt

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_class = None
        self.current_function = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            function_name = f"{self.current_class}.{node.name}"
        else:
            function_name = node.name
        self.current_function = function_name
        self.graph.add_node(function_name)
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.graph.add_edge(self.current_function, node.func.id)
            elif isinstance(node.func, ast.Attribute):
                self.graph.add_edge(self.current_function, f"{node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)

def generate_call_graph(source_code):
    tree = ast.parse(source_code)
    visitor = CallGraphVisitor()
    visitor.visit(tree)
    return visitor.graph

source_code = """
class MyClass:
    def method_a(self):
        self.method_b()
        self.method_c()

    def method_b(self):
        self.method_d()

    def method_c(self):
        pass

    def method_d(self):
        self.method_e()

    def method_e(self):
        pass

if __name__ == "__main__":
    obj = MyClass()
    obj.method_a()
"""

call_graph = generate_call_graph(source_code)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(call_graph)
nx.draw(call_graph, pos, with_labels=True, arrows=True)
plt.show()
