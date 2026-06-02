import pytest

from app.db.retrievers import retrieve_inventory, retrieve_suppliers
from tests.mock_database import MockDatabase
from fastapi.exceptions import HTTPException


@pytest.fixture
async def db_instance():
    db_instance = MockDatabase()
    await db_instance.setup()
    db = await db_instance.override_get_db()
    yield db
    await db_instance.teardown()


@pytest.mark.anyio
async def test_retrieve_inventory(db_instance):
    db_item = await retrieve_inventory("White Sugar", db_instance)
    assert db_item.name == "White Sugar"

@pytest.mark.anyio
async def test_retrieve_inventory(db_instance):
    try:
        await retrieve_inventory("Whit Sugar", db_instance)
    except HTTPException as ex:
        assert ex.status_code == 404
        assert ex.detail == "Ingredient not found in the database."
    except Exception as e:
        raise e

@pytest.mark.anyio
async def test_retrieve_suppliers(db_instance):
    retrieved_items =  await retrieve_suppliers(["Tehran Supply Co."], db_instance)
    assert "Tehran Supply Co." in [retrieved_item.name for retrieved_item in retrieved_items]


@pytest.mark.anyio
async def test_retrieve_suppliers(db_instance):
    try:
        await retrieve_suppliers(["Tehran SupplyCo."], db_instance)
    except HTTPException as ex:
        assert ex.status_code == 404
        assert ex.detail == "Supplier not found in the database."
    except Exception as e:
        raise e
