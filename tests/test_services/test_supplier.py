import pytest
from app.services.supplier import get_suppliers_for_ingredient



@pytest.mark.asyncio
async def test_retrieve_suppliers_for_ingredient_zero(db_instance):
    result = await get_suppliers_for_ingredient(db=db_instance, ingredient_id=4)
    assert result == []

@pytest.mark.asyncio
async def test_retrieve_suppliers_for_ingredient_one(db_instance):
    result = await get_suppliers_for_ingredient(db=db_instance, ingredient_id=2)
    assert [supp.name for supp in result] == ["Tehran Supply Co."]
