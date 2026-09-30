from app.analysis.parser import parse_python_file


file_path = (
    "storage/repositories/"
    "6ab2b019f6f0711568cc409f/"
    "extracted/lvs-project/"
    "app/routes/order_routes.py"
)

result = parse_python_file(file_path)

print("File:")
print(result["path"])

print("\nImports:")
for item in result["imports"]:
    print("-", item)

print("\nClasses:")
for item in result["classes"]:
    print("-", item)

print("\nFunctions:")

for function in result["functions"]:
    print("-", function["name"])

    print("  Arguments:")
    for argument in function["arguments"]:
        print("  -", argument)

    print("  Decorators:")
    for decorator in function["decorators"]:
        print("  -", decorator)