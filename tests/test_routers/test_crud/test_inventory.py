import pytest


from tests.parameters.routers.crud.inventory import (
    test_create_inventory_item_successful,
    test_create_inventory_item_wrong_supplier_fail,
    test_create_inventory_item_no_supplier_fail,
    test_duplicate_inventory_name_fail,
    test_multiple_suppliers_success,
    test_create_inventory_item_zero_quantity,
    test_create_inventory_item_missing_name_fail,
    test_create_inventory_item_negative_quantity_fail,
    test_get_inventory_filter_quantity_to,
    test_get_inventory_filter_quantity_to_from,
    test_get_one_inventory_item_suppliers,
    test_get_inventory_filter_quantity_from,
    test_get_inventory_by_name_multiple,
    test_get_all_inventory,
    test_get_inventory_filter_quantity_empty,
    test_get_wrong_format_inventory_item_fail,
    test_get_inventory_non_existent_id,
    test_get_inventory_by_name,
    test_get_inventory_filter_suppliers,
    test_get_ont_inventory_item,
    test_get_inventory_wrong_property,
    test_successful_delete_list,
    test_successful_delete,
    test_non_existing_resource_delete,
    test_wrong_format_delete,
    test_dependant_entity_delete_restrict,
    test_put_inventory_item_successful_name_and_supplier,
    test_put_inventory_item_fail_non_existing_attribute,
    test_put_inventory_item_successful_quantity,
    test_put_inventory_item_fail_validation,
    test_put_inventory_item_fail_type,
    test_put_inventory_item_fail_non_existing_entity,
    test_case_insert_single_supplier_success,
    test_case_insert_multiple_supplier_success,
    test_case_insert_wrong_datatype_fail,
    test_case_insert_wrong_endpoint_fail,
    test_case_insert_non_existing_ingredient_fail,
    test_case_insert_non_existing_supplier_fail,
    test_case_insert_wrong_datatype_fail_second_case


)

@pytest.mark.anyio
@pytest.mark.parametrize(
    "param_dict",
    [
        # post
        # test_create_inventory_item_successful,
        # test_create_inventory_item_wrong_supplier_fail,
        # test_create_inventory_item_no_supplier_fail,
        # test_create_inventory_item_negative_quantity_fail,
        # test_create_inventory_item_zero_quantity,
        # test_create_inventory_item_missing_name_fail,
        # test_duplicate_inventory_name_fail,
        # test_multiple_suppliers_success,
        # get
        # test_get_inventory_filter_quantity_to,
        # test_get_inventory_filter_quantity_to_from,
        # test_get_one_inventory_item_suppliers,
        # test_get_inventory_filter_quantity_from,
        # test_get_inventory_by_name_multiple,
        # test_get_all_inventory,
        # test_get_inventory_filter_quantity_empty,
        # test_get_wrong_format_inventory_item_fail,
        # test_get_inventory_non_existent_id,
        # test_get_inventory_by_name,
        # test_get_inventory_filter_suppliers,
        # test_get_ont_inventory_item,
        # test_get_inventory_wrong_property,
        # delete
        # test_successful_delete_list,
        # test_successful_delete,
        # test_non_existing_resource_delete,
        # test_wrong_format_delete,
        # test_dependant_entity_delete_restrict,
        # put
        # test_put_inventory_item_successful_name_and_supplier,
        # test_put_inventory_item_fail_non_existing_attribute,
        # test_put_inventory_item_successful_quantity,
        # test_put_inventory_item_fail_validation,
        # test_put_inventory_item_fail_type,
        # test_put_inventory_item_fail_non_existing_entity,
        # supplier ingredient relation
        test_case_insert_single_supplier_success,
        test_case_insert_multiple_supplier_success,
        test_case_insert_wrong_datatype_fail,
        test_case_insert_wrong_endpoint_fail,
        test_case_insert_non_existing_ingredient_fail,
        test_case_insert_non_existing_supplier_fail,
        test_case_insert_wrong_datatype_fail_second_case
    ],
)
async def test_inventory(blueprint_fixture, param_dict):
    await blueprint_fixture(param_dict)



#testing the modifications for upplier-ingredient relation

    #delete
        #fail
            #case1
            #case2
            #case3
            #case4
            #case5
            
    #insert
        #success
            #step1:get the orders and store them
            #step2:send the request
            #step3:make sure the status code is 201
            #step4:get the supplier for the ingredient
            #step5:make sure the get method for dependent suppliers contains the new one
            #step6:make sure the orders are not affected
        #fail
            # case1
            # case2
            # case3
            # case5



#case1: wrong data type
#case2: non existing inventory
#case3: non existing supplier
#case4: non eisting combination
#case5: wrong path

