from pathlib import Path
from zipfile import ZipFile


def extract_repository(zip_path: str, extract_path: str) -> Path:
    zip_file = Path(zip_path)
    destination = Path(extract_path)

    destination.mkdir(parents=True, exist_ok=True)

    with ZipFile(zip_file, "r") as archive:
        for member in archive.infolist():
            member_path = destination / member.filename

            if not member_path.resolve().is_relative_to(destination.resolve()):
                raise ValueError("Unsafe ZIP file path detected")

            if member.is_dir():
                member_path.mkdir(parents=True, exist_ok=True)
            else:
                member_path.parent.mkdir(parents=True, exist_ok=True)

                with archive.open(member) as source:
                    with open(member_path, "wb") as target:
                        target.write(source.read())
    return destination