from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user_id
from app.projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.projects.service import (
    create_new_project,
    delete_user_project,
    get_user_project,
    list_user_projects,
    update_user_project,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def project_to_response(project: dict) -> dict:
    return {
        "id": str(project["_id"]),
        "name": project["name"],
        "description": project.get("description"),
        "owner_id": str(project["owner_id"]),
    }


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectCreate,
    user_id: str = Depends(get_current_user_id),
):
    project = await create_new_project(
        name=data.name,
        description=data.description,
        owner_id=user_id,
    )

    return project_to_response(project)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def list_projects(
    user_id: str = Depends(get_current_user_id),
):
    projects = await list_user_projects(user_id)

    return [
        project_to_response(project)
        for project in projects
    ]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        project = await get_user_project(
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

    return project_to_response(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    user_id: str = Depends(get_current_user_id),
):
    try:
        project = await update_user_project(
            project_id,
            user_id,
            data.model_dump(exclude_unset=True),
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

    return project_to_response(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        await delete_user_project(
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