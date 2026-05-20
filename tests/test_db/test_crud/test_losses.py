import pytest
from tests.conftest import blueprint_fixture, test_now
from tests.test_db.test_crud.parameters.loss import (
    test_quantity_zero_fail,
    test_quantity_negative_fail,
    test_success_created,
    test_ingredient_name_not_in_database_fail
                                                     )

@pytest.mark.freeze_time(test_now)
@pytest.mark.parametrize(
"param_dict",
    [
        test_quantity_zero_fail,
        test_quantity_negative_fail,
        test_success_created,
        test_ingredient_name_not_in_database_fail
    ]
)
def test_orders(blueprint_fixture, param_dict):
    blueprint_fixture(param_dict)