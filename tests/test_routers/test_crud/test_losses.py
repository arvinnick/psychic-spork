import pytest
from tests.conftest import frozen_test_time
from tests.parameters.routers.crud.loss import (test_quantity_zero_fail,
                                                test_quantity_negative_fail,
                                                test_success_created,
                                                test_ingredient_name_not_in_database_fail,
                                                test_filter_quantity_lt,
                                                test_filter_quantity_gt_wrong_format,
                                                test_filter_quantity_lt_wrong_format,
                                                test_filter_quantity_gt,
                                                test_filter_datetime_to,
                                                test_filter_datetime_from,
                                                test_filter_datetime_from_to,
                                                test_filter_quantity_gt_lt,
                                                test_filter_datetime_to_wrong_format,
                                                test_filter_ingredient_id,
                                                test_filter_ingredient_id_wrong_format,
                                                test_success_singular_ingredient,
                                                test_success_singular,
                                                test_success_all,
                                                test_success_singular_id_non_existent,
                                                test_fail_wrong_sub_resources,
                                                ###delete
                                                test_non_existing_resource_delete,
                                                test_wrong_format_delete,
                                                test_successful_delete,
                                                test_fail_string_id
                                                )


@pytest.mark.anyio
@pytest.mark.freeze_time(frozen_test_time)
@pytest.mark.parametrize(
"param_dict",
    [
        ###########post
        test_quantity_zero_fail,
        test_quantity_negative_fail,
        test_success_created,
        test_ingredient_name_not_in_database_fail,
        ###########get
        test_filter_quantity_lt,
        test_filter_quantity_gt_wrong_format,
        test_filter_quantity_lt_wrong_format,
        test_filter_quantity_gt,
        test_filter_datetime_to,
        test_filter_datetime_from,
        test_filter_datetime_from_to,
        test_filter_quantity_gt_lt,
        test_filter_datetime_to_wrong_format,
        test_filter_ingredient_id,
        test_filter_ingredient_id_wrong_format,
        test_success_singular_ingredient,
        test_success_singular,
        test_success_all,
        test_success_singular_id_non_existent,
        test_fail_wrong_sub_resources,
        ############delete
        test_non_existing_resource_delete,
        test_wrong_format_delete,
        test_successful_delete,
        test_fail_string_id
    ]
)
async def test_losses(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)
