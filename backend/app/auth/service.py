from app.auth.dao import (
    create_user,
    get_user_by_email,
)
from app.auth.security import (
    hash_password,
    verify_password,
)


async def register_user(
    email: str,
    password: str,
) -> dict:

    existing_user = await get_user_by_email(email)

    if existing_user:
        raise ValueError("User already exists")

    hashed_password = hash_password(password)

    user_data = {
        "email": email,
        "password_hash": hashed_password,
    }

    return await create_user(user_data)


async def authenticate_user(
    email: str,
    password: str,
) -> dict | None:

    user = await get_user_by_email(email)

    if not user:
        return None

    if not verify_password(
        password,
        user["password_hash"],
    ):
        return None

    return user