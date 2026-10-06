import ast
from pathlib import Path

def extract_function_calls(function_node: ast.AST) -> list[dict]:
    calls = []

    for node in ast.walk(function_node):
        if not isinstance(node, ast.Call):
            continue

        call_name = None

        if isinstance(node.func, ast.Name):
            call_name = node.func.id

        elif isinstance(node.func, ast.Attribute):
            parts = []

            current = node.func

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            call_name = ".".join(reversed(parts))

        if call_name:
            calls.append(
                {
                    "name": call_name,
                    "line": node.lineno,
                }
            )

    return calls

def parse_python_file(file_path: str) -> dict:
    path = Path(file_path)

    source_code = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    tree = ast.parse(source_code)

    imports = []
    classes = []
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorators = []

            for decorator in node.decorator_list:
                decorators.append(ast.unparse(decorator))

            arguments = []

            for argument in node.args.args:
                arguments.append(argument.arg)

            calls = extract_function_calls(node)

            functions.append(
                {
                    "name": node.name,
                    "arguments": arguments,
                    "decorators": decorators,
                    "calls": calls,
                }
            )

    return {
        "path": str(path),
        "imports": imports,
        "classes": classes,
        "functions": functions,
    }