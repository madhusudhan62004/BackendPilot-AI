from app.analysis.discovery import discover_files

repository_path = "storage/repositories/6ab2b019f6f0711568cc409f/extracted/lvs-project"

files = discover_files(repository_path)

print(f"Total files: {len(files)}")

for file in files:
    print(file)