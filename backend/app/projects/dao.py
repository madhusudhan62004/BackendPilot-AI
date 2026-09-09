from bson import ObjectId

from app.core.database import database


project_collection = database["projects"]


async def create_project(project_data: dict) -> dict:
    result = await project_collection.insert_one(project_data)

    return await project_collection.find_one(
        {"_id": result.inserted_id}
    )


async def get_projects_by_owner(owner_id: str) -> list[dict]:
    cursor = project_collection.find(
        {"owner_id": ObjectId(owner_id)}
    )

    return await cursor.to_list(length=None)


async def get_project_by_id(project_id: str) -> dict | None:
    return await project_collection.find_one(
        {"_id": ObjectId(project_id)}
    )


async def update_project(
    project_id: str,
    update_data: dict,
) -> dict | None:

    await project_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": update_data},
    )

    return await get_project_by_id(project_id)


async def delete_project(project_id: str) -> bool:
    result = await project_collection.delete_one(
        {"_id": ObjectId(project_id)}
    )

    return result.deleted_count == 1