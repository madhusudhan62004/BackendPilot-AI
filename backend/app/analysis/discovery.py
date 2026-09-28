from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
}


def discover_files(repository_path: str) -> list[dict]:
    root = Path(repository_path)
    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        files.append(
            {
                "path": str(relative_path),
                "name": path.name,
                "extension": path.suffix,
                "size": path.stat().st_size,
            }
        )

    return files