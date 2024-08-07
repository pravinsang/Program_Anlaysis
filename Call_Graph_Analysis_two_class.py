import ast
import networkx as nx
import matplotlib.pyplot as plt

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_class = None
        self.current_function = None
        self.class_instances = {}

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

    def visit_Assign(self, node):
        if (isinstance(node.targets[0], ast.Attribute) and
                isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Name)):
            instance_name = node.targets[0].attr
            class_name = node.value.func.id
            self.class_instances[instance_name] = class_name
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_function:
            func_name = self.get_call_name(node.func)
            if func_name:
                self.graph.add_edge(self.current_function, func_name)
        self.generic_visit(node)

    def get_call_name(self, node):
        if isinstance(node, ast.Attribute):
            value_name = self.get_call_name(node.value)
            if value_name in self.class_instances:
                return f"{self.class_instances[value_name]}.{node.attr}"
            return f"{value_name}.{node.attr}"
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
        pass

    def method_d(self):
        self.method_e()

    def method_e(self):
        pass

class AnotherClass:
    def __init__(self):
        self.my_class_instance = MyClass()

    def method_x(self):
        self.method_y()
        self.method_z()

    def method_y(self):
        self.my_class_instance.method_a()  # Correctly calls method from MyClass instance

    def method_z(self):
        pass

if __name__ == "__main__":
    obj1 = MyClass()
    obj1.method_a()
    
    obj2 = AnotherClass()
    obj2.method_x()
"""

call_graph = generate_call_graph(source_code)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(call_graph)
nx.draw(call_graph, pos, with_labels=True, arrows=True)
plt.show()
