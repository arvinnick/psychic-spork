import pytest


from tests.parameters.routers.crud.inventory import (test_create_inventory_item_successful,
                                                     test_create_inventory_item_wrong_supplier_fail,
                                                     test_create_inventory_item_no_supplier_fail,
                                                     test_duplicate_inventory_name_fail,
                                                     test_multiple_suppliers_success,
                                                     test_create_inventory_item_zero_quantity,
                                                     test_create_inventory_item_missing_name_fail,
                                                     test_create_inventory_item_negative_quantity_fail)

@pytest.mark.anyio
@pytest.mark.parametrize(
"param_dict",
    [
        test_create_inventory_item_successful,
        test_create_inventory_item_wrong_supplier_fail,
        test_create_inventory_item_no_supplier_fail,
        test_create_inventory_item_negative_quantity_fail,
        test_create_inventory_item_zero_quantity,
        test_create_inventory_item_missing_name_fail,
        test_duplicate_inventory_name_fail,
        test_multiple_suppliers_success
    ]
)
async def test_inventory(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)


