from app.analysis.discovery import discover_files
from app.analysis.detector import (
    detect_frameworks,
    detect_languages,
)


repository_path = (
    "storage/repositories/"
    "6ab2b019f6f0711568cc409f/"
    "extracted/lvs-project"
)

files = discover_files(repository_path)

languages = detect_languages(files)
frameworks = detect_frameworks(repository_path)

print("Detected languages:")
for language in languages:
    print("-", language)

print("\nDetected frameworks:")
for framework in frameworks:
    print("-", framework)