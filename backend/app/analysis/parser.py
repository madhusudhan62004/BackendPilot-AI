import ast
from pathlib import Path


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

            functions.append(
                {
                    "name": node.name,
                    "arguments": arguments,
                    "decorators": decorators,
                }
            )

    return {
        "path": str(path),
        "imports": imports,
        "classes": classes,
        "functions": functions,
    }