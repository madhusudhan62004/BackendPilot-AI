from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.auth.dependencies import get_current_user_id
from app.repositories.schemas import RepositoryResponse
from app.repositories.service import (
    create_new_repository,
    delete_user_repository,
    get_user_repository,
    list_project_repositories,
    save_repository_file,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


def repository_to_response(repository: dict) -> dict:
    return {
        "id": str(repository["_id"]),
        "project_id": str(repository["project_id"]),
        "name": repository["name"],
        "source_type": repository["source_type"],
        "source_url": repository.get("source_url"),
        "status": repository["status"],
        "created_at": repository["created_at"],
    }

@router.post(
    "/project/{project_id}/upload",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_repository(
    project_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only ZIP files are supported",
        )

    try:
        # First verify that the user owns the project
        repository = await create_new_repository(
            project_id=project_id,
            owner_id=user_id,
            name=file.filename.removesuffix(".zip"),
            source_type="zip",
        )

        file_content = await file.read()

        await save_repository_file(
            repository_id=str(repository["_id"]),
            file_content=file_content,
        )

        repository = await get_user_repository(
            str(repository["_id"]),
            user_id,
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this project",
        )

    return repository_to_response(repository)

@router.get(
    "/project/{project_id}",
    response_model=list[RepositoryResponse],
)
async def list_repositories(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        repositories = await list_project_repositories(
            project_id,
            user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this project",
        )

    return [
        repository_to_response(repository)
        for repository in repositories
    ]


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
async def get_repository(
    repository_id: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        repository = await get_user_repository(
            repository_id,
            user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this repository",
        )

    return repository_to_response(repository)


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_repository(
    repository_id: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        await delete_user_repository(
            repository_id,
            user_id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this repository",
        )
