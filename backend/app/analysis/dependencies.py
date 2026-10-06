from pathlib import Path


def extract_import_dependencies(
    parsed_file: dict,
    repository_root: str,
) -> list[dict]:
    dependencies = []

    source_path = Path(parsed_file["path"])
    root = Path(repository_root)

    for imported_module in parsed_file["imports"]:
        if not imported_module.startswith("app."):
            continue

        module_parts = imported_module.split(".")

        # Try treating the final part as a symbol/function/class.
        # Example:
        # app.tasks.process_order_task
        # -> app/tasks.py
        module_parts_without_symbol = module_parts[:-1]

        possible_modules = [
            module_parts,
            module_parts_without_symbol,
        ]

        target_file = None

        for parts in possible_modules:
            module_path = root.joinpath(*parts)

            possible_files = [
                module_path.with_suffix(".py"),
                module_path / "__init__.py",
            ]

            for possible_file in possible_files:
                if possible_file.exists():
                    target_file = possible_file
                    break

            if target_file:
                break

        if target_file is None:
            continue

        dependencies.append(
            {
                "type": "import",
                "source": str(source_path),
                "target": str(target_file),
                "module": imported_module,
            }
        )

    return dependencies

def resolve_function_call(
    call_name: str,
    parsed_file: dict,
    all_parsed_files: list[dict],
) -> list[dict]:
    relationships = []

    # Ignore method calls where we don't have
    # an imported symbol to resolve.
    if "." in call_name:
        object_name, method_name = call_name.rsplit(".", 1)

        for imported in parsed_file["imports"]:
            imported_parts = imported.split(".")

            if imported_parts[-1] != object_name:
                continue

            imported_symbol = imported_parts[-1]

            for target_file in all_parsed_files:
                for function in target_file["functions"]:
                    if function["name"] == imported_symbol:
                        relationships.append(
                            {
                                "type": "function_call",
                                "source_file": parsed_file["path"],
                                "source_function": None,
                                "target_file": target_file["path"],
                                "target_function": imported_symbol,
                                "call": call_name,
                            }
                        )

    else:
        for target_file in all_parsed_files:
            for function in target_file["functions"]:
                if function["name"] == call_name:
                    relationships.append(
                        {
                            "type": "function_call",
                            "source_file": parsed_file["path"],
                            "source_function": None,
                            "target_file": target_file["path"],
                            "target_function": call_name,
                            "call": call_name,
                        }
                    )

    return relationships

def extract_function_relationships(
    parsed_file: dict,
    all_parsed_files: list[dict],
) -> list[dict]:
    relationships = []

    imported_symbols = {}

    for imported in parsed_file["imports"]:
        parts = imported.split(".")

        if len(parts) < 2:
            continue

        symbol = parts[-1]
        imported_symbols[symbol] = imported

    for function in parsed_file["functions"]:
        for call in function["calls"]:
            call_name = call["name"]

            if "." not in call_name:
                continue

            object_name, method_name = call_name.rsplit(".", 1)

            if object_name not in imported_symbols:
                continue

            imported_module = imported_symbols[object_name]

            for target_file in all_parsed_files:
                for target_function in target_file["functions"]:
                    if target_function["name"] != object_name:
                        continue

                    relationships.append(
                        {
                            "type": "function_call",
                            "source_file": parsed_file["path"],
                            "source_function": function["name"],
                            "target_file": target_file["path"],
                            "target_function": target_function["name"],
                            "call": call_name,
                            "line": call["line"],
                        }
                    )

    return relationships

def extract_resource_relationships(
    parsed_file: dict,
) -> list[dict]:
    relationships = []

    resource_names = set()

    for imported in parsed_file["imports"]:
        if imported.startswith("app.database."):
            resource_names.add(imported.split(".")[-1])

    for function in parsed_file["functions"]:
        for call in function["calls"]:
            call_name = call["name"]

            if "." not in call_name:
                continue

            object_name, method_name = call_name.rsplit(".", 1)

            if object_name not in resource_names:
                continue

            relationships.append(
                {
                    "type": "resource_call",
                    "source_file": parsed_file["path"],
                    "source_function": function["name"],
                    "resource": object_name,
                    "operation": method_name,
                    "line": call["line"],
                }
            )

    return relationships