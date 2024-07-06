# Code Analysis and Visualization Tool

This article explains a Python script that analyzes and visualizes the structure and dependencies of a Python project. The tool performs static code analysis, creates a graph representation of the code structure, and generates a visual graph of the project's components and their relationships.

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Code Structure](#code-structure)
4. [Key Components](#key-components)
5. [Usage](#usage)

## Overview

This tool is designed to help developers understand the structure and dependencies of their Python projects. It performs the following main tasks:

1. Analyzes Python source code files in a given project directory.
2. Extracts information about function definitions, class definitions, variable assignments, and their usages.
3. Creates a graph representation of the code structure.
4. Generates a visual graph showing the relationships between different components of the project.

## Dependencies

The script relies on the following Python libraries:

```python
import ast
import os
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
```

- `ast`: For parsing Python source code into an Abstract Syntax Tree (AST).
- `os`: For file and directory operations.
- `collections.defaultdict`: For creating nested dictionaries with default values.
- `networkx`: For creating and manipulating graphs.
- `matplotlib.pyplot`: For visualizing the graph.

## Code Structure

The code is organized into several main components:

1. `CodeAnalyzer` class: Handles the parsing and analysis of individual Python files.
2. `analyze_file` function: Analyzes a single Python file using the `CodeAnalyzer`.
3. `analyze_project` function: Analyzes an entire Python project by iterating through its files.
4. `create_graph` function: Creates a graph representation of the analyzed project.
5. `visualize_graph` function: Generates a visual representation of the graph.

## Key Components

### CodeAnalyzer Class

The `CodeAnalyzer` class is a subclass of `ast.NodeVisitor` and is responsible for traversing the AST of Python files. It keeps track of definitions and usages of functions, classes, variables, and methods.

Key methods:

```python
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        # ... initialization ...

    def visit_FunctionDef(self, node):
        # ... handle function definitions ...

    def visit_ClassDef(self, node):
        # ... handle class definitions ...

    def visit_Assign(self, node):
        # ... handle variable assignments ...

    def visit_Name(self, node):
        # ... handle variable usages ...

    def visit_Call(self, node):
        # ... handle function and method calls ...

    def get_context(self):
        # ... determine the current context ...
```

### Project Analysis

The `analyze_project` function walks through the project directory, analyzes each Python file, and aggregates the results:

```python
def analyze_project(project_path):
    # ... project analysis logic ...
```

### Graph Creation and Visualization

The `create_graph` function builds a `networkx.DiGraph` object based on the analysis results:

```python
def create_graph(analysis):
    # ... graph creation logic ...
```

The `visualize_graph` function uses `matplotlib` to create a visual representation of the graph:

```python
def visualize_graph(G):
    # ... graph visualization logic ...
```

## Usage

To use the tool, simply specify the path to your Python project and run the script:

```python
project_path = './sample_project'
analysis = analyze_project(project_path)
G = create_graph(analysis)
visualize_graph(G)

print("Graph has been saved as 'code_graph.png'")
```

This will analyze the project, create a graph representation, and save a visualization of the graph as "code_graph.png" in the current directory.

The resulting graph provides a visual overview of the project structure, showing relationships between functions, classes, and variables across different files in the project.