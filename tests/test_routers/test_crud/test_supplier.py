import pytest

from tests.conftest import test_now
from tests.test_routers.test_crud.parameters.supplier import (test_create_supplier_phone_number_wrong_fail,
                                                              test_create_supplier_success,
                                                              test_create_supplier_wrong_email_format_fail,
                                                              test_create_supplier_no_contact_fail
                                                              )
@pytest.mark.anyio
@pytest.mark.freeze_time(test_now)
@pytest.mark.parametrize(
"param_dict",
    [
        test_create_supplier_phone_number_wrong_fail,
        test_create_supplier_success,
        test_create_supplier_wrong_email_format_fail,
        test_create_supplier_no_contact_fail
    ]
)
async def test_orders(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)

@pytest.mark.anyio
async def test_ground_truth_test():
    #this is a test to make sure the CICD is working
    assert True