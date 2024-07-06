```markdown
# CodeAnalyzer: A Python Code Analysis Tool

## Introduction

The `CodeAnalyzer` is a Python tool designed to analyze the structure and dependencies of a Python project. It uses the Abstract Syntax Tree (AST) to parse Python files, tracking definitions and usages of classes, functions, methods, and variables. This tool is particularly useful for understanding the relationships within a codebase, aiding in refactoring, and ensuring code maintainability.

## Table of Contents

1. [Imports and Dependencies](#imports-and-dependencies)
2. [Code Structure Overview](#code-structure-overview)
3. [Class: CodeAnalyzer](#class-codeanalyzer)
4. [Function: analyze_file](#function-analyze_file)
5. [Function: analyze_project](#function-analyze_project)
6. [Function: create_graph](#function-create_graph)
7. [Function: visualize_graph](#function-visualize_graph)
8. [Usage Examples](#usage-examples)
9. [Error Handling and Edge Cases](#error-handling-and-edge-cases)
10. [Performance Considerations](#performance-considerations)
11. [Testing and Debugging](#testing-and-debugging)
12. [Configuration and Customization](#configuration-and-customization)
13. [Role in the Overall Architecture](#role-in-the-overall-architecture)
14. [Known Limitations and Future Improvements](#known-limitations-and-future-improvements)
15. [Contribution Guidelines](#contribution-guidelines)
16. [Summary](#summary)
17. [Major Updates](#major-updates)

## Imports and Dependencies

- `ast`: Provides AST nodes for parsing Python code.
- `os`: Used for file path operations.
- `defaultdict`: From `collections`, used for creating dictionaries with default values.
- `networkx as nx`: A library for creating and manipulating complex networks.
- `matplotlib.pyplot as plt`: Used for visualizing the graph.

## Code Structure Overview

The code is structured around the `CodeAnalyzer` class and several functions:
- `CodeAnalyzer`: Parses the AST and collects definitions and usages.
- `analyze_file`: Analyzes a single Python file.
- `analyze_project`: Recursively analyzes all Python files in a project.
- `create_graph`: Creates a network graph from the analysis data.
- `visualize_graph`: Visualizes the graph using `matplotlib`.

## Class: CodeAnalyzer

### API Explanation

**Purpose:**
- Parses Python code to track definitions and usages of code elements.

**Methods:**
- `__init__`: Initializes the analyzer with data structures to store definitions and usages.
- `visit_FunctionDef`: Tracks function definitions.
- `visit_ClassDef`: Tracks class definitions.
- `visit_Assign`: Tracks variable assignments.
- `visit_Name`: Tracks variable usages.
- `visit_Call`: Tracks function and method calls.
- `get_context`: Returns the current context (class or function).

### Internal Workings

The `CodeAnalyzer` uses the `ast.NodeVisitor` to traverse the AST. It maintains context information to track where definitions and usages occur. This information is stored in nested `defaultdict` structures.

### Code Snippets

```python
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.definitions = defaultdict(lambda: defaultdict(set))
        self.usages = defaultdict(lambda: defaultdict(list))
```

### Algorithms and Data Structures

- **Data Structures:** `defaultdict` for storing definitions and usages.
- **Algorithms:** Depth-first traversal of the AST using `ast.NodeVisitor`.

### Interactions

- Interacts with the `ast` module to parse and traverse the AST.
- Collects data that is used by `analyze_file` and `analyze_project`.

## Function: analyze_file

### API Explanation

**Purpose:**
- Analyzes a single Python file and returns definitions and usages.

**Parameters:**
- `file_path` (str): The path to the Python file.
- `relative_path` (str): The relative path of the file within the project.

**Return Value:**
- Tuple: (`definitions`, `usages`), both are `defaultdict` structures.

### Internal Workings

- Reads the file content and parses it into an AST.
- Uses `CodeAnalyzer` to visit the AST nodes and collect data.

### Code Snippets

```python
def analyze_file(file_path, relative_path):
    with open(file_path, 'r') as file:
        content = file.read()
    tree = ast.parse(content)
    analyzer = CodeAnalyzer()
    analyzer.current_file = relative_path
    analyzer.visit(tree)
    return analyzer.definitions, analyzer.usages
```

## Function: analyze_project

### API Explanation

**Purpose:**
- Recursively analyzes all Python files in a project.

**Parameters:**
- `project_path` (str): The root path of the project.

**Return Value:**
- Dictionary: Contains `definitions` and `usages` for the entire project.

### Internal Workings

- Walks through the project directory, finding all `.py` files.
- Calls `analyze_file` for each file and aggregates the results.

### Code Snippets

```python
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
                # Aggregate definitions and usages
    return project_analysis
```

## Function: create_graph

### API Explanation

**Purpose:**
- Creates a directed graph from the analysis data.

**Parameters:**
- `analysis` (dict): Contains `definitions` and `usages`.

**Return Value:**
- `networkx.DiGraph`: The graph representing the code structure and dependencies.

### Internal Workings

- Adds nodes for each definition.
- Adds edges for each usage, connecting the source (function or method) to the target (variable, function, or method).

### Code Snippets

```python
def create_graph(analysis):
    G = nx.DiGraph()
    for def_type, def_dict in analysis['definitions'].items():
        for name, locations in def_dict.items():
            node_id = f"{def_type}:{name}"
            G.add_node(node_id, type=def_type, name=name, locations=locations)
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
```

## Function: visualize_graph

### API Explanation

**Purpose:**
- Visualizes the graph using `matplotlib`.

**Parameters:**
- `G` (networkx.DiGraph): The graph to visualize.

### Internal Workings

- Uses `networkx` and `matplotlib` to draw the graph.
- Saves the visualization as an image file.

### Code Snippets

```python
def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    labels = {node: f"{data['type']}:\n{data['name']}" for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Code Structure and Dependencies")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("code_graph.png", format="png", dpi=300)
    plt.close()
```

## Usage Examples

### Setup

1. Ensure `networkx` and `matplotlib` are installed:
    ```bash
    pip install networkx matplotlib
    ```

2. Place the `CodeAnalyzer` code in a Python file, e.g., `code_analyzer.py`.

### Common Use Cases

- Analyze a project and visualize the code structure:
    ```python
    project_path = './sample_project'
    analysis = analyze_project(project_path)
    G = create_graph(analysis)
    visualize_graph(G)
    print("Graph has been saved as 'code_graph.png'")
    ```

### Example Input/Outputs

- **Input:** A directory containing Python files.
- **Output:** A graph visualization saved as `code_graph.png`.

## Error Handling and Edge Cases

- **File Reading Errors:** The `analyze_file` function uses a `with open` statement, which handles file reading errors gracefully.
- **AST Parsing Errors:** The `ast.parse` function may raise exceptions if the file content is not valid Python code. These should be caught and handled appropriately.

## Performance Considerations

- **Large Projects:** The recursive file traversal and AST parsing can be time-consuming for large projects. Consider parallelizing the file analysis or optimizing the AST traversal.
- **Graph Creation:** The `create_graph` function can become slow for large graphs. Optimize the graph creation process or use more efficient graph libraries if necessary.

## Testing and Debugging

- **Unit Tests:** Write unit tests for each function to ensure they handle various edge cases and input scenarios.
- **Integration Tests:** Test the entire workflow on sample projects to ensure the tool produces accurate results.
- **Debugging:** Use logging to trace the execution and data flow within the tool.

## Configuration and Customization

- **Exclusion Lists:** Allow users to specify files or directories to exclude from the analysis.
- **Output Formats:** Support additional output formats for the graph visualization, such as JSON or DOT.

## Role in the Overall Architecture

- **Code Maintenance:** Helps developers understand and maintain large codebases.
- **Refactoring:** Aids in identifying dependencies and potential refactoring targets.
- **Documentation:** Provides a visual representation of the code structure, supplementing traditional documentation.

## Known Limitations and Future Improvements

- **Performance:** Improve performance for very large projects.
- **Incomplete Coverage:** Currently, only top-level definitions and usages are tracked. Improve coverage of nested and lambda functions.
- **User Interface:** Develop a web-based UI for easier interaction and visualization.

## Contribution Guidelines

- **Bug Reports:** Use the project's issue tracker to report bugs.
- **Feature Requests:** Propose new features via the issue tracker.
- **Pull Requests:** Ensure tests are added for new functionality. Follow the project's coding standards and guidelines.

## Summary

The `CodeAnalyzer` is a powerful tool for analyzing Python projects, providing insights into code structure and dependencies. It aids in understanding, maintaining, and refactoring codebases, making it an essential tool for developers.

## Major Updates

- **Version 1.0:** Initial release of the `CodeAnalyzer` tool.
```

This wiki article provides a comprehensive guide to the `CodeAnalyzer` tool, covering its purpose, structure, usage, and development considerations. It is designed to help developers understand and utilize the tool effectively.