from app.core.database import database


user_collection = database["users"]


async def create_user(user_data: dict) -> dict:
    result = await user_collection.insert_one(user_data)

    created_user = await user_collection.find_one(
        {"_id": result.inserted_id}
    )

    return created_user


async def get_user_by_email(email: str) -> dict | None:
    return await user_collection.find_one({"email": email})