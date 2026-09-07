import pytest

from app.projects.dao import create_project


@pytest.mark.anyio
async def test_create_project():

    project_data = {
        "name": "Test BackendPilot",
        "description": "Testing MongoDB",
        "owner_id": "test-user-id",
    }

    project = await create_project(project_data)

    assert project is not None
    assert project["name"] == "Test BackendPilot"