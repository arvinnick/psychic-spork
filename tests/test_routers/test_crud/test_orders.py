import pytest
from tests.conftest import frozen_test_time
from tests.parameters.routers.crud.orders import (test_create_order_item_successful,
                                                  test_ingredient_not_in_database_fail,
                                                  test_supplier_not_in_database_fail,
                                                  test_create_order_supplier_mismatch_fail)


@pytest.mark.anyio
@pytest.mark.freeze_time(frozen_test_time)
@pytest.mark.parametrize(
"param_dict",
    [
        test_create_order_item_successful,
        test_ingredient_not_in_database_fail,
        test_supplier_not_in_database_fail,
        test_create_order_supplier_mismatch_fail,
    ]
)
async def test_orders(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)