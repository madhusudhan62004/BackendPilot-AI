from pathlib import Path


def detect_entity_type(file_path: str) -> str | None:
    path = Path(file_path)

    if "app" in path.parts:
        app_index = path.parts.index("app")
        repository_parts = set(path.parts[app_index:])

        filename = path.stem.lower()

        if "routes" in repository_parts or "routers" in repository_parts:
            return "route"

        if "services" in repository_parts or "service" in filename:
            return "service"

        if "tasks" in repository_parts or "task" in filename:
            return "task"

        if "models" in repository_parts or "model" in filename:
            return "model"

        if (
            "database" in filename
            or "db" in repository_parts
            or "repositories" in repository_parts
            or "dao" in repository_parts
        ):
            return "database"

    return None

def extract_endpoints(parsed_file: dict) -> list[dict]:
    endpoints = []

    for function in parsed_file["functions"]:
        for decorator in function["decorators"]:
            if not decorator.startswith("router."):
                continue

            decorator_call = decorator[len("router."):]

            if "(" not in decorator_call:
                continue

            method, remainder = decorator_call.split("(", 1)

            path = remainder.rsplit(")", 1)[0].strip()

            if (
                len(path) >= 2
                and path[0] in {"'", '"'}
                and path[-1] == path[0]
            ):
                path = path[1:-1]

            if method.lower() not in {
                "get",
                "post",
                "put",
                "delete",
                "patch",
                "options",
                "head",
            }:
                continue

            endpoints.append(
                {
                    "type": "endpoint",
                    "method": method.upper(),
                    "path": path,
                    "function": function["name"],
                    "file": parsed_file["path"],
                }
            )

    return endpoints

def extract_file_entity(parsed_file: dict) -> dict | None:
    entity_type = detect_entity_type(parsed_file["path"])

    if entity_type is None:
        return None

    entity = {
        "type": entity_type,
        "file": parsed_file["path"],
    }

    if entity_type == "service":
        entity["functions"] = [
            function["name"]
            for function in parsed_file["functions"]
        ]

    elif entity_type == "model":
        entity["classes"] = parsed_file["classes"]

    elif entity_type == "database":
        entity["imports"] = parsed_file["imports"]
    
    elif entity_type == "task":
        entity["functions"] = [
            function["name"]
            for function in parsed_file["functions"]
        ]

    return entity