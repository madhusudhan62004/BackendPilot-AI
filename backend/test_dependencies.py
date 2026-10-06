from pathlib import Path

from app.analysis.discovery import discover_files
from app.analysis.parser import parse_python_file
from app.analysis.dependencies import extract_function_relationships
from app.analysis.dependencies import (
    extract_resource_relationships
)

repository_root = Path(
    "storage/repositories/"
    "6ab2b019f6f0711568cc409f/"
    "extracted/lvs-project"
)

discovered_files = discover_files(str(repository_root))

parsed_files = []

for file in discovered_files:
    if file["extension"] != ".py":
        continue

    file_path = repository_root / file["path"]

    parsed_files.append(
        parse_python_file(str(file_path))
    )


for parsed_file in parsed_files:
    relationships = extract_function_relationships(
        parsed_file,
        parsed_files,
    )

    if not relationships:
        continue

    print(f"\nFile: {parsed_file['path']}")

    for relationship in relationships:
        print(relationship)


    resource_relationships = extract_resource_relationships(
        parsed_file
    )

    for relationship in resource_relationships:
        print(relationship)