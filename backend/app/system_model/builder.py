
from pathlib import Path

from app.analysis.discovery import discover_files
from app.analysis.detector import detect_languages, detect_frameworks
from app.analysis.parser import parse_python_file
from app.analysis.entities import extract_file_entity, extract_endpoints
from app.analysis.dependencies import (
    extract_import_dependencies,
    extract_function_relationships,
    extract_resource_relationships,
)

from app.system_model.schemas import (
    UnifiedSystemModel,
    RepositoryInfo,
    SourceLocation,
    SystemNode,
    SystemRelationship,
    RelationshipEvidence,
    SystemModelStats,
)

def _relative_path(file_path: str, root: Path) -> str:
    return Path(file_path).resolve().relative_to(root).as_posix()

def _node_id(node_type: str, path: str, name: str) -> str:
    return f"{node_type}:{path}:{name}"

def _add_relationship(
    relationships: dict,
    relationship_type: str,
    source_id: str,
    target_id: str,
    file_path: str,
    line: int | None = None,
    expression: str | None = None,
):
    relationship_id = (
        f"{relationship_type}:{source_id}:{target_id}"
    )

    relationships[relationship_id] = SystemRelationship(
        id=relationship_id,
        type=relationship_type,
        source_id=source_id,
        target_id=target_id,
        evidence=RelationshipEvidence(
            file_path=file_path,
            line=line,
            expression=expression,
        ),
    )

def build_system_model(
    repository_id: str,
    repository_name: str,
    repository_path: str,
) -> UnifiedSystemModel:

    root = Path(repository_path).resolve()

    # 1. Discover repository files
    discovered_files = discover_files(str(root))

    # 2. Detect languages and frameworks
    languages = detect_languages(discovered_files)
    frameworks = detect_frameworks(str(root))

    nodes = {}
    relationships = {}

    parsed_files = []
    file_entities = {}

    # 3. Create file nodes and parse Python files
    for file_info in discovered_files:
        relative_path = file_info["path"]
        file_id = _node_id("file", relative_path, "file")

        parsed_file = None
        entity = None

        if file_info["extension"].lower() == ".py":
            absolute_path = root / relative_path

            try:
                parsed_file = parse_python_file(str(absolute_path))
                entity = extract_file_entity(parsed_file)
                parsed_files.append(parsed_file)

            except (SyntaxError, UnicodeDecodeError):
                # Keep the file in the model even if parsing fails.
                pass

        file_entities[relative_path] = entity

        nodes[file_id] = SystemNode(
            id=file_id,
            type="file",
            name=file_info["name"],
            role=entity["type"] if entity else None,
            source=SourceLocation(path=relative_path),
            metadata={
                "extension": file_info["extension"],
                "size": file_info["size"],
            },
        )

        # 4. Add function and class nodes
        if parsed_file is None:
            continue

        for function in parsed_file["functions"]:
            function_id = _node_id(
                "function", relative_path, function["name"]
            )

            nodes[function_id] = SystemNode(
                id=function_id,
                type="function",
                name=function["name"],
                source=SourceLocation(path=relative_path),
                metadata={
                    "arguments": function["arguments"],
                    "decorators": function["decorators"],
                },
            )

            _add_relationship(
                relationships,
                "contains",
                file_id,
                function_id,
                relative_path,
            )

        for class_name in parsed_file["classes"]:
            class_id = _node_id(
                "class", relative_path, class_name
            )

            nodes[class_id] = SystemNode(
                id=class_id,
                type="class",
                name=class_name,
                source=SourceLocation(path=relative_path),
            )

            _add_relationship(
                relationships,
                "contains",
                file_id,
                class_id,
                relative_path,
            )

        # 5. Add API endpoint nodes
        for endpoint in extract_endpoints(parsed_file):
            endpoint_name = (
                f"{endpoint['method']} {endpoint['path']}"
            )

            endpoint_id = _node_id(
                "endpoint", relative_path, endpoint_name
            )

            handler_id = _node_id(
                "function",
                relative_path,
                endpoint["function"],
            )

            nodes[endpoint_id] = SystemNode(
                id=endpoint_id,
                type="endpoint",
                name=endpoint_name,
                source=SourceLocation(path=relative_path),
                metadata={
                    "method": endpoint["method"],
                    "path": endpoint["path"],
                    "handler": endpoint["function"],
                },
            )

            _add_relationship(
                relationships,
                "exposes",
                file_id,
                endpoint_id,
                relative_path,
            )

            if handler_id in nodes:
                _add_relationship(
                    relationships,
                    "handled_by",
                    endpoint_id,
                    handler_id,
                    relative_path,
                )

    # 6. Add file import relationships
    for parsed_file in parsed_files:
        source_path = _relative_path(parsed_file["path"], root)
        source_id = _node_id("file", source_path, "file")

        for dependency in extract_import_dependencies(
            parsed_file, str(root)
        ):
            try:
                target_path = _relative_path(
                    dependency["target"], root
                )
            except ValueError:
                continue

            target_id = _node_id("file", target_path, "file")

            if target_id not in nodes:
                continue

            _add_relationship(
                relationships,
                "imports",
                source_id,
                target_id,
                source_path,
                expression=dependency["module"],
            )

    # 7. Add function-call relationships
    for parsed_file in parsed_files:
        source_path = _relative_path(parsed_file["path"], root)

        for relationship in extract_function_relationships(
            parsed_file, parsed_files
        ):
            try:
                target_path = _relative_path(
                    relationship["target_file"], root
                )
            except ValueError:
                continue

            source_function_id = _node_id(
                "function",
                source_path,
                relationship["source_function"],
            )

            target_function_id = _node_id(
                "function",
                target_path,
                relationship["target_function"],
            )

            if (
                source_function_id not in nodes
                or target_function_id not in nodes
            ):
                continue

            _add_relationship(
                relationships,
                "calls",
                source_function_id,
                target_function_id,
                source_path,
                line=relationship.get("line"),
                expression=relationship["call"],
            )

    # 8. Add resource nodes and access relationships
    for parsed_file in parsed_files:
        source_path = _relative_path(parsed_file["path"], root)

        for relationship in extract_resource_relationships(
            parsed_file
        ):
            resource_name = relationship["resource"]

            resource_id = _node_id(
                "resource", "infrastructure", resource_name
            )

            if resource_id not in nodes:
                nodes[resource_id] = SystemNode(
                    id=resource_id,
                    type="resource",
                    name=resource_name,
                    source=SourceLocation(path=source_path),
                    metadata={"kind": "infrastructure"},
                )

            function_id = _node_id(
                "function",
                source_path,
                relationship["source_function"],
            )

            if function_id not in nodes:
                continue

            _add_relationship(
                relationships,
                "accesses",
                function_id,
                resource_id,
                source_path,
                line=relationship.get("line"),
                expression=(
                    f"{resource_name}.{relationship['operation']}"
                ),
            )

    # 9. Assemble the Unified System Model
    return UnifiedSystemModel(
        repository=RepositoryInfo(
            repository_id=repository_id,
            name=repository_name,
            languages=languages,
            frameworks=frameworks,
        ),
        nodes=list(nodes.values()),
        relationships=list(relationships.values()),
        stats=SystemModelStats(
            file_count=len(discovered_files),
            node_count=len(nodes),
            relationship_count=len(relationships),
        ),
    )