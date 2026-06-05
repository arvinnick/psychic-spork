"""
Hardcoded stuff for the tests
"""
import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.db.database import get_db
from app.main import app
from tests.mock_database import MockDatabase

frozen_test_time = "2026-05-20T15:40:22"



@pytest_asyncio.fixture()
async def db_instance():
    db_instance = MockDatabase()
    await db_instance.setup()
    db = await db_instance.override_get_db()
    yield db
    await db_instance.teardown()



@pytest_asyncio.fixture()
async def blueprint_fixture():
    mock_db = MockDatabase()
    await mock_db.setup()
    app.dependency_overrides[get_db] = mock_db.override_get_db
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        async def blueprint(param_dict,
                      client = ac):
            """
            this is a blueprint for the testcases, assuming that most of them are just going to send a request to the server,
            then check the status code and response payload.
            """
            req_url = param_dict["req_url"]
            req_json = param_dict["req_json"]
            res_status_code = param_dict["res_status_code"]
            res_json = param_dict["res_json"]
            response = await client.post(req_url, json=req_json)
            assert response.status_code == res_status_code, str(response.json())
            assert response.json() == res_json
        yield blueprint
        await mock_db.teardown()
        app.dependency_overrides.clear()


