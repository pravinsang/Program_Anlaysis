import ast
import networkx as nx
import matplotlib.pyplot as plt

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_class = None
        self.current_function = None
        self.visited_functions = set()

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            function_name = f"{self.current_class}.{node.name}"
        else:
            function_name = node.name
        
        # Ensure each function is visited only once
        if function_name not in self.visited_functions:
            self.current_function = function_name
            self.graph.add_node(function_name)
            self.visited_functions.add(function_name)
            self.generic_visit(node)
            self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            func_name = self.get_call_name(node.func)
            if func_name:
                self.graph.add_edge(self.current_function, func_name)
        self.generic_visit(node)

    def get_call_name(self, node):
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "self" and self.current_class:
                return f"{self.current_class}.{node.attr}"
            else:
                value_name = self.get_call_name(node.value)
                return f"{value_name}.{node.attr}" if value_name else None
        elif isinstance(node, ast.Name):
            return node.id
        return None

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
        self.method_e()
        self.method_d()
        self.method_a()

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
