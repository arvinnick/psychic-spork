import pytest
from tests.conftest import test_now
from tests.test_routers.test_crud.parameters.loss import (
    test_quantity_zero_fail,
    test_quantity_negative_fail,
    test_success_created,
    test_ingredient_name_not_in_database_fail
                                                     )
@pytest.mark.anyio
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
async def test_losses(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)