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
test_case_singular_ingredient_successful = {
    "req_url": "/crud/orders/1", #todo: implement the hashid
    "method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": 1,
                    "date_time": "2023-11-01T10:00:00.00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}


test_case_multiple_ingredient_successful = {
    "req_url": "/crud/orders?id=1&id=2",#todo: implement the hashid
    "method": "get",
    "res_status_code": 200,
    "res_json":{
                    "id": hash(1),
                    "date_time": "2023-11-01T10:00:00.00:00", #note that the datetime format might be wrong. So don't get stressed if the test didn't pass for the first time. Just fix the hardcodes
                    "quantity": 100.0,
                    "ingredient_id": 1,
                    "supplier_id": 1
                }
}