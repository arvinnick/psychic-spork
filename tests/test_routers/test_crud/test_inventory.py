import pytest


from tests.parameters.routers.crud.inventory import (
    test_create_inventory_item_successful,
    test_create_inventory_item_wrong_supplier_fail,
    test_create_inventory_item_no_supplier_fail,
    test_duplicate_inventory_name_fail,
    test_multiple_suppliers_success,
    test_create_inventory_item_zero_quantity,
    test_create_inventory_item_missing_name_fail,
    test_create_inventory_item_negative_quantity_fail,
    test_get_inventory_filter_quantity_to,
    test_get_inventory_filter_quantity_to_from,
    test_get_one_inventory_item_suppliers,
    test_get_inventory_filter_quantity_from,
    test_get_inventory_by_name_multiple,
    test_get_all_inventory,
    test_get_inventory_filter_quantity_empty,
    test_get_wrong_format_inventory_item_fail,
    test_get_inventory_non_existent_id,
    test_get_inventory_by_name,
    test_get_inventory_filter_suppliers,
    test_get_ont_inventory_item,
    test_get_inventory_wrong_property,
    test_successful_delete_list,
    test_successful_delete,
    test_non_existing_resource_delete,
    test_wrong_format_delete
)

@pytest.mark.anyio
@pytest.mark.parametrize(
"param_dict",
    [
        #post
        # test_create_inventory_item_successful,
        # test_create_inventory_item_wrong_supplier_fail,
        # test_create_inventory_item_no_supplier_fail,
        # test_create_inventory_item_negative_quantity_fail,
        # test_create_inventory_item_zero_quantity,
        # test_create_inventory_item_missing_name_fail,
        # test_duplicate_inventory_name_fail,
        # test_multiple_suppliers_success,
        # # get
        # test_get_inventory_filter_quantity_to,
        # test_get_inventory_filter_quantity_to_from,
        # test_get_one_inventory_item_suppliers,
        # test_get_inventory_filter_quantity_from,
        # test_get_inventory_by_name_multiple,
        # test_get_all_inventory,
        # test_get_inventory_filter_quantity_empty,
        # test_get_wrong_format_inventory_item_fail,
        # test_get_inventory_non_existent_id,
        # test_get_inventory_by_name,
        # test_get_inventory_filter_suppliers,
        # test_get_ont_inventory_item,
        # test_get_inventory_wrong_property,
        #delete
        test_successful_delete_list,
        # test_successful_delete,
        # test_non_existing_resource_delete,
        # test_wrong_format_delete
    ]
)
async def test_inventory(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)


