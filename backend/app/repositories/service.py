from datetime import datetime, timezone
from bson import ObjectId
from pathlib import Path
from app.analysis.extractor import extract_repository
from app.projects.service import get_user_project
from app.repositories.dao import (
    create_repository,
    delete_repository,
    get_repositories_by_project,
    get_repository_by_id,
    update_repository
)


async def create_new_repository(
    project_id: str,
    owner_id: str,
    name: str,
    source_type: str,
    source_url: str | None = None,
) -> dict:
    # Verify that the user owns the project
    await get_user_project(project_id, owner_id)

    now = datetime.now(timezone.utc)

    repository_data = {
        "project_id": ObjectId(project_id),
        "name": name,
        "source_type": source_type,
        "source_url": source_url,
        "status": "uploaded",
        "created_at": now,
        "updated_at": now,
    }

    return await create_repository(repository_data)


async def list_project_repositories(
    project_id: str,
    owner_id: str,
) -> list[dict]:
    # Verify that the user owns the project
    await get_user_project(project_id, owner_id)

    return await get_repositories_by_project(project_id)


async def get_user_repository(
    repository_id: str,
    owner_id: str,
) -> dict:
    repository = await get_repository_by_id(repository_id)

    if not repository:
        raise ValueError("Repository not found")

    project_id = str(repository["project_id"])

    # Verify that the user owns the parent project
    await get_user_project(project_id, owner_id)

    return repository

async def delete_user_repository(
    repository_id: str,
    owner_id: str,
) -> None:
    repository = await get_user_repository(
        repository_id,
        owner_id,
    )

    deleted = await delete_repository(
        str(repository["_id"])
    )

    if not deleted:
        raise ValueError("Repository not found")

    storage_path = repository.get("storage_path")

    if storage_path:
        repository_dir = Path(storage_path).parent

        if repository_dir.exists():
            import shutil

            shutil.rmtree(repository_dir)

async def save_repository_file(
    repository_id: str,
    file_content: bytes,
) -> str:
    storage_dir = Path("storage") / "repositories" / repository_id
    storage_dir.mkdir(parents=True, exist_ok=True)

    file_path = storage_dir / "repository.zip"

    # Save uploaded ZIP
    file_path.write_bytes(file_content)

    # Update storage path
    await update_repository(
        repository_id,
        {
            "storage_path": str(file_path),
            "updated_at": datetime.now(timezone.utc),
        },
    )

    extract_path = storage_dir / "extracted"

    try:
        # Mark extraction as in progress
        await update_repository(
            repository_id,
            {
                "status": "extracting",
                "updated_at": datetime.now(timezone.utc),
            },
        )

        # Extract repository
        extract_repository(
            str(file_path),
            str(extract_path),
        )

        # Mark extraction as successful
        await update_repository(
            repository_id,
            {
                "status": "extracted",
                "updated_at": datetime.now(timezone.utc),
            },
        )
        updated_repository = await get_repository_by_id(repository_id)
        print("STATUS AFTER EXTRACTION:", updated_repository["status"])

    except Exception:
        # Mark extraction as failed
        await update_repository(
            repository_id,
            {
                "status": "failed",
                "updated_at": datetime.now(timezone.utc),
            },
        )

        raise

    return str(file_path)