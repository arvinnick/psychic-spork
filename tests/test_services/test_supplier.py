import pytest
from app.services.supplier import retrieve_suppliers_for_ingredient
from tests.conftest import db_instance



@pytest.mark.asyncio
async def test_retrieve_suppliers_for_ingredient_zero(db_instance):
    ingredient = "Peanut"
    result = await retrieve_suppliers_for_ingredient(ingredient, db_instance)
    assert result == []

@pytest.mark.asyncio
async def test_retrieve_suppliers_for_ingredient_one(db_instance):
    ingredient = "White Sugar"
    result = await retrieve_suppliers_for_ingredient(ingredient, db_instance)
    assert [supp.name for supp in result] == ["Tehran Supply Co."]
