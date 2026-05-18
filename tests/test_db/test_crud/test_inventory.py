import pytest

from tests.conftest import blueprint_fixture
from tests.test_db.test_crud.parameters.inventory import (test_create_inventory_item_successful,
                                                          test_create_inventory_item_wrong_supplier_fail,
                                                          test_create_inventory_item_no_supplier_fail,
                                                          test_duplicate_inventory_name_fail,
                                                          test_multiple_suppliers_success,
                                                          test_create_inventory_item_zero_quantity,
                                                          test_create_inventory_item_missing_name_fail,
                                                          test_create_inventory_item_negative_quantity_fail)


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
def test_inventory(blueprint_fixture, param_dict):
    blueprint_fixture(param_dict)


