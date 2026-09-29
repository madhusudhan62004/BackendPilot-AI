from pathlib import Path


EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
}


FRAMEWORK_PACKAGE_MAP = {
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "celery": "Celery",
    "express": "Express",
    "nestjs": "NestJS",
}


def detect_languages(files: list[dict]) -> list[str]:
    languages = set()

    for file in files:
        extension = file["extension"].lower()

        language = EXTENSION_LANGUAGE_MAP.get(extension)

        if language:
            languages.add(language)

    return sorted(languages)


def detect_frameworks(repository_path: str) -> list[str]:
    root = Path(repository_path)

    requirements_file = root / "requirements.txt"

    if not requirements_file.exists():
        return []

    dependencies = requirements_file.read_text(
        encoding="utf-8",
        errors="ignore",
    ).lower()

    frameworks = set()

    for package_name, framework_name in FRAMEWORK_PACKAGE_MAP.items():
        if package_name in dependencies:
            frameworks.add(framework_name)

    return sorted(frameworks)