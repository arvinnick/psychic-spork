from tests.conftest import frozen_test_time


"""
post method
"""
#Test case: ingredient is not in the inventory (no entity)
test_ingredient_not_in_database_fail = {"req_url": "/crud/orders/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat",
                                                                "supplier": "Tehran Supply Co.",
                                                            },
                                                  "res_status_code": 404,
                                                  "res_json": {
                                                      'detail': 'Ingredient not found in the database.'
                                                  }
    ,
                                        }

#Test case: Order created successfully
test_create_order_item_successful = {
    "req_url": "/crud/orders/",
    "req_json": {
        "quantity": 1.0,
        "ingredient": "White Sugar",
        "supplier": "Tehran Supply Co.",
    },
    "res_status_code": 201,
    'res_json': {
        "date_time": frozen_test_time,
        'ingredient': {
            "name": "White Sugar",
            "quantity": 200.0,
'suppliers': [
    {
        'address': '1st Valiasr St, Tehran',
        'email': 'info@tehransupply.com',
        'name': 'Tehran Supply Co.',
        'number': 'tel:+98-21-1234-5678'
     }
              ]

        },
                 'quantity': 1.0,
                 'supplier':
                     {
                         'name': 'Tehran Supply Co.',
                         'address': '1st Valiasr St, Tehran',
                         'number': 'tel:+98-21-1234-5678',
                         'email': 'info@tehransupply.com'
                     }

                 },
}

#Test case: wrong supplier
test_supplier_not_in_database_fail = {"req_url": "/crud/orders/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "White Sugar",
                                                                "supplier": "Aramco",
                                                            },
                                                  "res_status_code": 404,
                                                  "res_json": {
                                                      'detail': 'Supplier not found in the database.'
                                                  }
    ,
                                      }

#Test case: supplier doesn't provide the ingredient
test_create_order_supplier_mismatch_fail = {
    "req_url": "/crud/orders/",
    "req_json": {
        "quantity": 1.0,
        "ingredient": "White Sugar",
        "supplier": "South Trading",
    },
    "res_status_code": 400,
    "res_json":{
        "detail":"non of the mentioned suppliers provide the requested ingredient."
    },
}

"""
get method
"""

test_case_all_orders_successful                             = {
    "req_url": "/crud/orders",
    "method": "get",
    "res_status_code": 200,
    "res_json":[
        {
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
        {
            "date_time": "2023-11-01T10:00:00",
            "quantity": 50.0,
            "ingredient_id": 3,
            "supplier_id": 2
        }
    ]
}

test_case_singular_order_successful                             = {
    "req_url": "/crud/orders/1",
    "method": "get",
    "res_status_code": 200,
    "res_json":{
                    "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}

test_case_multiple_orders_successful                            = {
    "req_url": "/crud/orders?order_id=1&order_id=2",
    "method": "get",
    "res_status_code": 200,
    "res_json":[
        {
                "id": 1,
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
        {
            "id": 2,
            "date_time": "2023-11-01T10:00:00",
            "quantity": 50.0,
            "ingredient_id": 3,
            "supplier_id": 2
        }
    ]
}

test_case_singular_ingredient_successful                        = {
    "req_url": "/crud/orders?ingredient_id=1",
"method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": 1,
                    "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}

test_case_multiple_ingredient_successful                        = {
    "req_url": "/crud/orders?ingredient_id=1&ingredient_id=3",
"method": "get",
    "res_status_code": 200,
    "res_json":[
        {
                "id": 1,
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
        {
            "id": 2,
            "date_time": "2023-11-01T10:00:00",
            "quantity": 50.0,
            "ingredient_id": 3,
            "supplier_id": 2
        }
    ]
}

test_case_singular_supplier_successful                          = {
    "req_url": "/crud/orders?supplier_id=1",
"method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": 1,
                    "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}

test_case_multiple_supplier_successful                          = {
    "req_url": "/crud/orders?supplier_id=1&supplier_id=2",
"method": "get",
    "res_status_code": 200,
    "res_json":[
        {
                "id": 1,
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
        {
            "id": 2,
            "date_time": "2023-11-01T10:00:00",
            "quantity": 50.0,
            "ingredient_id": 3,
            "supplier_id": 2
        }
    ]
}

test_case_ingredient_supplier_combination_successful            = {
    "req_url": "/crud/orders?supplier_id=1&supplier_id=3",
"method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": 1,
                    "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}

test_case_ingredient_supplier_combination_successful_not_found  = {
    "req_url": "/crud/orders?supplier_id=1&supplier_id=1",
"method": "get",
    "res_status_code": 200,
    "res_json":{}
}

test_case_wrong_format_fail                                     = {
    "req_url": "/crud/orders?supplier_id=a",
"method": "get",
    "res_status_code": 422,
    "res_json":{}
}

test_case_between_two_dates_successful                          = {
    "req_url": "/crud/orders?date_time_from=2023-10-01T00:00:00&date_time_to=2023-12-01T00:00:00",
"method": "get",
    "res_status_code": 200,
    "res_json":[
        {
                "id": 1,
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
        {
            "id": 2,
            "date_time": "2023-11-01T10:00:00",
            "quantity": 50.0,
            "ingredient_id": 3,
            "supplier_id": 2
        }
    ]
}


test_case_between_two_dates_successful_not_found                = {
"req_url": "/crud/orders?date_time_from=2023-08-01T00:00:00&date_time_to=2023-09-01T00:00:00",
"method": "get",
    "res_status_code": 200,
    "res_json":{}
}

test_case_datetime_not_correctly_formatted_failure              = {
"req_url": "/crud/orders?date_time_from=ds&date_time_to=2023-09-01T00:00:00",
"method": "get",
    "res_status_code": 422,
    "res_json":{}
}

test_case_between_two_quantities_successful                     = {
"req_url": "/crud/orders?quantity_gt=80&quantity_lt=120",
"method": "get",
    "res_status_code": 200,
    "res_json":{
                "id": 1,
                "date_time": "2023-11-01T10:00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            }
}


test_case_string_as_id_failure                                  = {
"req_url": "/crud/orders/as",
"method": "get",
    "res_status_code": 400  ,
    "res_json":{}
}

test_case_string_not_a_valid_id_failure                         = {
"req_url": "/crud/orders/4",
"method": "get",
    "res_status_code": 404  ,
    "res_json":{}
}

test_case_retrieve_suppliers_successful                         = {
"req_url": "/crud/orders/2/suppliers",
"method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": 2,
                    "name": "South Trading",
                    "address": "Coastal Blvd, Bandar Abbas",
                    "number": 'tel:+98-76-1234-5678',
                    "email": None
                }
}

test_case_retrieve_ingredient_successful                        = {
"req_url": "/crud/orders/1/ingredients",
"method": "get",
    "res_status_code": 200,
    "res_json":{"id": 1, "name": "Wheat Flour", "quantity": 500.5}
}