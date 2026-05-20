from tests.conftest import MockDatabase, test_now

from datetime import datetime

database = MockDatabase()
date_time = datetime.now()

#Test case: ingredient is not in the inventory (no entity)
test_ingredient_not_in_database_fail = {"req_url": "/crud/orders/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat",
                                                                "supplier": "Tehran Supply Co.",
                                                            },
                                                  "res_status_code": 400,
                                                  "res_json": {
                                                      'detail': 'Ingredient not found in the database.'
                                                  }
    ,
                                                  "get_db": database.override_db_dependency}

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
        "date_time": test_now,
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
"get_db":database.override_db_dependency
}

#Test case: wrong supplier
test_supplier_not_in_database_fail = {"req_url": "/crud/orders/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "White Sugar",
                                                                "supplier": "Aramco",
                                                            },
                                                  "res_status_code": 400,
                                                  "res_json": {
                                                      'detail': 'Supplier not found in the database.'
                                                  }
    ,
                                                  "get_db": database.override_db_dependency}

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
"get_db":database.override_db_dependency
}




