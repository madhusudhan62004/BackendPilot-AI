from app.analysis.entities import (
    detect_entity_type,
    extract_endpoints,
    extract_file_entity,
)
from app.analysis.parser import parse_python_file


repository_root = (
    "storage/repositories/"
    "6ab2b019f6f0711568cc409f/"
    "extracted/lvs-project"
)


files = [
    "app/routes/order_routes.py",
    "app/services/vendor_service.py",
    "app/models/model.py",
    "app/database.py",
    "app/tasks.py",
]


for relative_path in files:
    file_path = f"{repository_root}/{relative_path}"

    parsed_file = parse_python_file(file_path)

    entity = extract_file_entity(parsed_file)

    print(f"\nFile: {relative_path}")
    print("Entity:")
    print(entity)

    if entity and entity["type"] == "route":
        endpoints = extract_endpoints(parsed_file)

        print("Endpoints:")
        for endpoint in endpoints:
            print(endpoint)