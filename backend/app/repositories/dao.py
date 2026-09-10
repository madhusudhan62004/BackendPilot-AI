from bson import ObjectId

from app.core.database import database


repository_collection = database["repositories"]


async def create_repository(repository_data: dict) -> dict:
    result = await repository_collection.insert_one(repository_data)

    return await repository_collection.find_one(
        {"_id": result.inserted_id}
    )


async def get_repository_by_id(repository_id: str) -> dict | None:
    return await repository_collection.find_one(
        {"_id": ObjectId(repository_id)}
    )


async def get_repositories_by_project(project_id: str) -> list[dict]:
    cursor = repository_collection.find(
        {"project_id": ObjectId(project_id)}
    )

    return await cursor.to_list(length=None)


async def delete_repository(repository_id: str) -> bool:
    result = await repository_collection.delete_one(
        {"_id": ObjectId(repository_id)}
    )

    return result.deleted_count == 1

async def update_repository(
    repository_id: str,
    update_data: dict,
) -> dict | None:
    await repository_collection.update_one(
        {"_id": ObjectId(repository_id)},
        {"$set": update_data},
    )

    return await get_repository_by_id(repository_id)