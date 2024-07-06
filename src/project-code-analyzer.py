import ast
import os
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class CodeAnalyzer(ast.NodeVisitor):
    
    def __init__(self):
        self.definitions = defaultdict(lambda: defaultdict(set))
        self.usages = defaultdict(lambda: defaultdict(list))
        self.current_file = ""
        self.current_class = None
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.definitions['function'][node.name].add((self.current_file, node.lineno))
        parent_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = parent_function

    def visit_ClassDef(self, node):
        self.definitions['class'][node.name].add((self.current_file, node.lineno))
        parent_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = parent_class

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.definitions['variable'][target.id].add((self.current_file, node.lineno))
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            context = self.get_context()
            self.usages['variable'][node.id].append((self.current_file, node.lineno, context))
        self.generic_visit(node)

    def visit_Call(self, node):
        context = self.get_context()
        if isinstance(node.func, ast.Name):
            self.usages['function'][node.func.id].append((self.current_file, node.func.lineno, context))
        elif isinstance(node.func, ast.Attribute):
            self.usages['method'][node.func.attr].append((self.current_file, node.func.lineno, context))
        self.generic_visit(node)

    def get_context(self):
        if self.current_class and self.current_function:
            return f"{self.current_class}.{self.current_function}"
        elif self.current_function:
            return self.current_function
        elif self.current_class:
            return self.current_class
        return None

def analyze_file(file_path, relative_path):
    with open(file_path, 'r') as file:
        content = file.read()
    tree = ast.parse(content)
    analyzer = CodeAnalyzer()
    analyzer.current_file = relative_path
    analyzer.visit(tree)
    return analyzer.definitions, analyzer.usages

def analyze_project(project_path):
    project_analysis = {
        'definitions': defaultdict(lambda: defaultdict(set)),
        'usages': defaultdict(lambda: defaultdict(list))
    }

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, project_path)
                definitions, usages = analyze_file(full_path, relative_path)
                for def_type, def_dict in definitions.items():
                    for name, locations in def_dict.items():
                        project_analysis['definitions'][def_type][name].update(locations)
                for usage_type, usage_dict in usages.items():
                    for name, locations in usage_dict.items():
                        project_analysis['usages'][usage_type][name].extend(locations)

    return project_analysis

def create_graph(analysis):
    G = nx.DiGraph()
    
    # Add nodes
    for def_type, def_dict in analysis['definitions'].items():
        for name, locations in def_dict.items():
            node_id = f"{def_type}:{name}"
            G.add_node(node_id, type=def_type, name=name, locations=locations)

    # Add edges
    for usage_type, usage_dict in analysis['usages'].items():
        for name, locations in usage_dict.items():
            for loc in locations:
                file, line, context = loc
                if context:
                    source_id = f"function:{context}" if '.' not in context else f"method:{context}"
                    target_id = f"{usage_type}:{name}"
                    if G.has_node(source_id) and G.has_node(target_id):
                        G.add_edge(source_id, target_id, file=file, line=line)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    
    # Draw labels
    labels = {node: f"{data['type']}:\n{data['name']}" for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    

    plt.title("Code Structure and Dependencies")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("code_graph.png", format="png", dpi=300)
    plt.close()


# Usage
project_path = './sample_project'
analysis = analyze_project(project_path)
G = create_graph(analysis)
visualize_graph(G)

print("Graph has been saved as 'code_graph.png'")