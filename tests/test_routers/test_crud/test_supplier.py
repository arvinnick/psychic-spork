import pytest

from tests.conftest import frozen_test_time
from tests.parameters.routers.crud.supplier import (test_create_supplier_phone_number_wrong_fail,
                                                    test_create_supplier_success,
                                                    test_create_supplier_wrong_email_format_fail,
                                                    test_create_supplier_no_contact_fail,
                                                    test_get_single_supplier_success,
                                                    test_get_single_non_existent_supplier_success,
                                                    test_get_supplier_ingredients_success,
                                                    test_get_all_suppliers_success,
                                                    test_get_single_supplier_wrong_format,
                                                    test_get_supplier_wrong_property
                                                    )
@pytest.mark.anyio
@pytest.mark.freeze_time(frozen_test_time)
@pytest.mark.parametrize(
"param_dict",
    [
        ####post
        test_create_supplier_phone_number_wrong_fail,
        test_create_supplier_success,
        test_create_supplier_wrong_email_format_fail,
        test_create_supplier_no_contact_fail,

        ####get
        test_get_single_supplier_success,
        test_get_single_non_existent_supplier_success,
        # test_get_supplier_ingredients_success, #todo: make it after finishing the inventory get because you will use its services here
        test_get_all_suppliers_success,
        test_get_single_supplier_wrong_format,
        test_get_supplier_wrong_property
    ]
)
async def test_orders(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)

@pytest.mark.anyio
async def test_ground_truth_test():
    #this is a test to make sure the CICD is working
    assert True