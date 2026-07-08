import pytest

from app.db.retrievers import retrieve_inventory, retrieve_suppliers_by_name
from fastapi.exceptions import HTTPException

from app.core.logger import logger

@pytest.mark.anyio
async def test_retrieve_inventory(db_instance):
    db_item = await retrieve_inventory(ingredient_name="White Sugar",
                                       db=db_instance)
    db_obj = db_item.first()
    assert db_obj.name == "White Sugar"

@pytest.mark.anyio
async def test_retrieve_inventory_not_found(db_instance):
    objs = await retrieve_inventory(db_instance, ingredient_name="Whit Sugar")
    assert objs.all() == []

@pytest.mark.anyio
async def test_retrieve_suppliers(db_instance):
    retrieved_items =  await retrieve_suppliers_by_name(["Tehran Supply Co."], db_instance)
    assert "Tehran Supply Co." in [retrieved_item.name for retrieved_item in retrieved_items]


@pytest.mark.anyio
async def test_retrieve_suppliers_not_found(db_instance):
    try:
        await retrieve_suppliers_by_name(["Tehran SupplyCo."], db_instance)
    except HTTPException as ex:
        assert ex.status_code == 204
        assert ex.detail == "Supplier not found in the database."
    except Exception as e:
        logger.error(f"An error occurred while testing supplier retrieval: {str(e)}")
        raise e
