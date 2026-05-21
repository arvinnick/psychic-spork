import pytest
from tests.conftest import test_now
from tests.test_db.test_crud.parameters.orders import (test_create_order_item_successful,
                                                       test_ingredient_not_in_database_fail,
                                                       test_supplier_not_in_database_fail,
                                                       test_create_order_supplier_mismatch_fail
                                                       )

@pytest.mark.freeze_time(test_now)
@pytest.mark.parametrize(
"param_dict",
    [
        test_create_order_item_successful,
        test_ingredient_not_in_database_fail,
        test_supplier_not_in_database_fail,
        test_create_order_supplier_mismatch_fail,
    ]
)
def test_orders(blueprint_fixture, param_dict):
    blueprint_fixture(param_dict)