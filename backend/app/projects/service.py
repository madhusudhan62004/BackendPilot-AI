from datetime import datetime, timezone
from bson import ObjectId
from app.projects.dao import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects_by_owner,
    update_project,
)


async def create_new_project(
    name: str,
    description: str | None,
    owner_id: str,
) -> dict:

    now = datetime.now(timezone.utc)

    project_data = {
        "name": name,
        "description": description,
        "owner_id": ObjectId(owner_id),
        "created_at": now,
        "updated_at": now,
    }

    return await create_project(project_data)


async def list_user_projects(
    owner_id: str,
) -> list[dict]:

    return await get_projects_by_owner(owner_id)


async def get_user_project(
    project_id: str,
    owner_id: str,
) -> dict:

    project = await get_project_by_id(project_id)

    if not project:
        raise ValueError("Project not found")

    if str(project["owner_id"]) != owner_id:
        raise PermissionError("You do not own this project")

    return project


async def update_user_project(
    project_id: str,
    owner_id: str,
    update_data: dict,
) -> dict:

    project = await get_user_project(
        project_id,
        owner_id,
    )

    if not update_data:
        return project

    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_project = await update_project(
        project_id,
        update_data,
    )

    return updated_project


async def delete_user_project(
    project_id: str,
    owner_id: str,
) -> None:

    await get_user_project(
        project_id,
        owner_id,
    )

    deleted = await delete_project(project_id)

    if not deleted:
        raise ValueError("Project not found")