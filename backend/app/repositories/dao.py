from bson import ObjectId

from app.core.database import database


repository_collection = database["repositories"]


async def create_repository(repository_data: dict) -> dict:
    result = await repository_collection.insert_one(repository_data)

    return await repository_collection.find_one(
        {"_id": result.inserted_id}
    )


async def get_repository(repository_id: str) -> dict | None:
    return await repository_collection.find_one(
        {"_id": ObjectId(repository_id)}
    )


async def get_repositories_by_project(
    project_id: str,
) -> list[dict]:

    cursor = repository_collection.find(
        {"project_id": project_id}
    )

    return await cursor.to_list(length=None)