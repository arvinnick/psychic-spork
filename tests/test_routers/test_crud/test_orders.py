import pytest
from tests.conftest import frozen_test_time
from tests.parameters.routers.crud.orders import (test_create_order_item_successful,
                                                test_ingredient_not_in_database_fail,
                                                test_supplier_not_in_database_fail,
                                                test_create_order_supplier_mismatch_fail,
                                                test_case_singular_order_successful,
                                                test_case_multiple_orders_successful,
                                                test_case_singular_ingredient_successful,
                                                test_case_multiple_ingredient_successful,
                                                test_case_singular_supplier_successful,
                                                test_case_multiple_supplier_successful,
                                                test_case_ingredient_supplier_combination_successful,
                                                test_case_ingredient_supplier_combination_successful_not_found,
                                                test_case_wrong_format_fail,
                                                test_case_between_two_dates_successful,
                                                test_case_between_two_dates_successful_not_found,
                                                test_case_datetime_not_correctly_formatted_failure,
                                                test_case_between_two_quantities_successful,
                                                test_case_string_as_id_failure,
                                                test_case_string_not_a_valid_id_failure,
                                                test_case_retrieve_suppliers_successful,
                                                test_case_retrieve_ingredient_successful,
                                                test_case_retrieve_wrong_property,
                                                test_case_successful_delete_list,
                                                test_wrong_format_delete,
                                                test_non_existing_resource_delete,
                                                test_case_successful_delete,
                                                test_case_all_orders_successful,
                                                update_fail_supplier_not_providing_ingredient,
                                                update_fail_negative_quantity,
                                                update_fail_ingredient_not_existing,
                                                update_fail_supplier_not_existing,
                                                update_success_supplier_id,
                                                update_success_ingredient_id,
                                                update_success_quantity,
                                                update_success_date_time
                                                  )


@pytest.mark.anyio
@pytest.mark.freeze_time(frozen_test_time)
@pytest.mark.parametrize(
"param_dict",
    [
        ###create
        # test_create_order_item_successful,
        # test_ingredient_not_in_database_fail,
        # test_supplier_not_in_database_fail,
        # test_create_order_supplier_mismatch_fail,
        ###read
        # test_case_singular_order_successful,
        # test_case_multiple_orders_successful,
        # test_case_singular_ingredient_successful,
        # test_case_multiple_ingredient_successful,
        # test_case_singular_supplier_successful,
        # test_case_multiple_supplier_successful,
        # test_case_ingredient_supplier_combination_successful,
        # test_case_ingredient_supplier_combination_successful_not_found,
        # test_case_wrong_format_fail,
        # test_case_between_two_dates_successful,
        # test_case_between_two_dates_successful_not_found,
        # test_case_datetime_not_correctly_formatted_failure,
        # test_case_between_two_quantities_successful,
        # test_case_string_as_id_failure,
        # test_case_string_not_a_valid_id_failure,
        # test_case_retrieve_suppliers_successful,
        # test_case_retrieve_ingredient_successful,
        # test_case_retrieve_wrong_property,
        # test_case_all_orders_successful,
        ###delete
        # test_case_successful_delete_list,
        # test_wrong_format_delete,
        # test_non_existing_resource_delete,
        # test_case_successful_delete,
        ###update
        update_fail_supplier_not_providing_ingredient,
        # update_fail_negative_quantity,
        # update_fail_ingredient_not_existing,
        # update_fail_supplier_not_existing,
        # update_success_supplier_id,
        # update_success_ingredient_id,
        # update_success_quantity,
        # update_success_date_time
]
)
async def test_orders(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)