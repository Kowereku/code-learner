import ast

CONSTRUCTS = {
    ast.While: "while",
    ast.For: "for",
    ast.If: "if",
    ast.FunctionDef: "def",
    ast.Return: "return",
    ast.List: "list",
    ast.Dict: "dict",
}


def constructs(tree: ast.AST) -> set[str]:
    """Return the constructs used in a parsed program."""
    nodes = list(ast.walk(tree))
    found = {CONSTRUCTS[type(node)] for node in nodes if type(node) in CONSTRUCTS}
    if any(isinstance(node, ast.If) and node.orelse for node in nodes):
        found.add("else")
    return found


def passes_python_checks(answer: str, reference: str) -> bool:
    """Return whether the answer is valid Python that uses every construct of the reference."""
    try:
        tree = ast.parse(answer)
    except SyntaxError:
        return False
    return constructs(ast.parse(reference)) <= constructs(tree)
