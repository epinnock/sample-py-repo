# CodeAnalyzer: A Comprehensive Guide

## Introduction

The `CodeAnalyzer` is a sophisticated tool designed to parse and analyze Python codebases, providing detailed insights into the structure, dependencies, and usage of code elements such as classes, functions, and variables. This tool is particularly useful for developers looking to understand, refactor, or optimize large codebases by visualizing relationships and dependencies between different parts of the code.

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
16. [Major Updates and Documentation History](#major-updates-and-documentation-history)

## Imports and Dependencies

- `ast`: Provides tools for processing Python abstract syntax trees (ASTs).
- `os`: Offers functions for interacting with the operating system, used here for file path manipulations.
- `collections.defaultdict`: A dictionary subclass that provides default values for missing keys, simplifying the collection of definitions and usages.
- `networkx as nx`: A powerful library for creating, manipulating, and studying the structure, dynamics, and functions of complex networks.
- `matplotlib.pyplot as plt`: A plotting library used for visualizing the graph of code dependencies.

## Code Structure Overview

The code is structured around a main class `CodeAnalyzer` and several functions that facilitate the analysis of individual files and entire projects. The class uses Python's `ast` module to traverse and analyze the abstract syntax tree of Python code, collecting data on definitions and usages of various code elements.

## Class: CodeAnalyzer

### Purpose

The `CodeAnalyzer` class is designed to traverse and analyze Python code's abstract syntax tree, collecting data on definitions and usages of classes, functions, and variables.

### Methods

- `__init__`: Initializes the analyzer with data structures to hold definitions and usages.
- `visit_FunctionDef`, `visit_ClassDef`, `visit_Assign`, `visit_Name`, `visit_Call`: These methods override the `NodeVisitor` methods to handle specific types of nodes in the AST, recording the relevant information.
- `get_context`: Determines the current context (class or function) for recording usages.

### Internal Workings

The class uses a combination of overridden `NodeVisitor` methods and custom methods to traverse the AST, recording the location and context of each definition and usage.

### Code Snippet

```python
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.definitions = defaultdict(lambda: defaultdict(set))
        self.usages = defaultdict(lambda: defaultdict(list))
        self.current_file = ""
        self.current_class = None
        self.current_function = None
```

### Data Structures

- `defaultdict`: Used to store definitions and usages, providing default values for missing keys.

### Interactions

The class interacts with the `ast` module to traverse and analyze the AST, and with the `analyze_file` and `analyze_project` functions to provide analysis results.

## Function: analyze_file

### Purpose

Analyzes a single Python file, returning the definitions and usages found in the file.

### Parameters

- `file_path` (str): The full path to the file to be analyzed.
- `relative_path` (str): The relative path of the file within the project.

### Return Value

- Tuple of two dictionaries: `definitions` and `usages`.

### Code Snippet

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

### Purpose

Analyzes an entire project directory, aggregating the results from individual file analyses.

### Parameters

- `project_path` (str): The path to the root directory of the project.

### Return Value

- Dictionary containing aggregated `definitions` and `usages`.

### Code Snippet

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
                for def_type, def_dict in definitions.items():
                    for name, locations in def_dict.items():
                        project_analysis['definitions'][def_type][name].update(locations)
                for usage_type, usage_dict in usages.items():
                    for name, locations in usage_dict.items():
                        project_analysis['usages'][usage_type][name].extend(locations)

    return project_analysis
```

## Function: create_graph

### Purpose

Creates a directed graph representing the relationships and dependencies between different code elements.

### Parameters

- `analysis` (dict): The analysis results from `analyze_project`.

### Return Value

- `networkx.DiGraph`: A directed graph representing the code structure and dependencies.

### Code Snippet

```python
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
```

## Function: visualize_graph

### Purpose

Visualizes the graph created by `create_graph` using `matplotlib`.

### Parameters

- `G` (networkx.DiGraph): The graph to be visualized.

### Code Snippet

```python
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
```

## Usage Examples

### Setup

1. Ensure all dependencies are installed:
    ```bash
    pip install ast os collections networkx matplotlib
    ```

2. Place the `CodeAnalyzer` code in a Python file, e.g., `code_analyzer.py`.

### Common Use Cases

- Analyze a single file:
    ```python
    definitions, usages = analyze_file('path/to/file.py', 'relative/path/to/file.py')
    ```

- Analyze an entire project:
    ```python
    analysis = analyze_project('path/to/project')
    ```

- Create and visualize the graph:
    ```python
    G = create_graph(analysis)
    visualize_graph(G)
    ```

### Example Input/Output

- Input:
    ```python
    project_path = './sample_project'
    analysis = analyze_project(project_path)
    G = create_graph(analysis)
    visualize_graph(G)
    ```

- Output:
    ```
    Graph has been saved as 'code_graph.png'
    ```

## Error Handling and Edge Cases

The tool is designed to handle common errors gracefully, such as file not found or syntax errors in Python files. Edge cases include handling of nested classes and functions, and multiple assignments in a single statement.

## Performance Considerations

The tool's performance is largely dependent on the size of the codebase being analyzed. For large projects, consider parallelizing the file analysis or optimizing the graph creation and visualization processes.

## Testing and Debugging

- Unit tests should be created for each function and method to ensure correctness.
- Use logging to track the progress and debug issues during the analysis.

## Configuration and Customization

- The tool can be extended to include additional code elements or to customize the graph visualization.

## Role in the Overall Architecture

The `CodeAnalyzer` is a standalone tool that can be integrated into larger development workflows for code analysis and visualization.

## Known Limitations and Future Improvements

- The tool currently does not handle dynamic imports or code executed conditionally.
- Future improvements could include support for more complex code structures and better visualization options.

## Contribution Guidelines

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that your code is well-documented and includes tests.

## Major Updates and Documentation History

- **Version 1.0**: Initial release of the `CodeAnalyzer` tool.

## Summary

The `CodeAnalyzer` is a powerful tool for analyzing and visualizing Python codebases, providing developers with valuable insights into code structure, dependencies, and usage. Its modular design and extensibility make it a valuable asset for any development team looking to understand and optimize their code.