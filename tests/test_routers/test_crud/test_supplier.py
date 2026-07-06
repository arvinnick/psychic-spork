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
                                                    test_get_supplier_wrong_property,
                                                    test_case_get_list,
                                                    test_case_successful_delete,
                                                    test_wrong_format_delete,
                                                    test_non_existing_resource_delete,
                                                    test_case_successful_delete_list,
                                                    test_case_update_success_email,
                                                    test_case_update_success_name,
                                                    test_case_update_success_phone,
                                                    test_case_update_fail_non_existing_attribute,
                                                    test_case_update_fail_email,
                                                    test_case_update_fail_phone,
                                                    test_case_update_fail_non_existing_supplier
                                                    )
@pytest.mark.anyio
@pytest.mark.freeze_time(frozen_test_time)
@pytest.mark.parametrize(
"param_dict",
    [
        # ####post
        # test_create_supplier_phone_number_wrong_fail,
        # test_create_supplier_success,
        # test_create_supplier_wrong_email_format_fail,
        # test_create_supplier_no_contact_fail,
        # ####get
        # test_get_single_supplier_success,
        # test_get_single_non_existent_supplier_success,
        # test_get_supplier_ingredients_success,
        # test_get_all_suppliers_success,
        # test_get_single_supplier_wrong_format,
        # test_get_supplier_wrong_property,
        # test_case_get_list,
        # ##delete
        # test_case_successful_delete,
        # test_wrong_format_delete,
        # test_non_existing_resource_delete,
        # test_case_successful_delete_list,
        ##put
        test_case_update_success_email,
        # test_case_update_success_name,
        # test_case_update_success_phone,
        # test_case_update_fail_non_existing_attribute,
        # test_case_update_fail_email,
        # test_case_update_fail_phone,
        # test_case_update_fail_non_existing_supplier
    ]
)
async def test_suppliers(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)

@pytest.mark.anyio
async def test_ground_truth_test():
    #this is a test to make sure the CICD is working
    assert True