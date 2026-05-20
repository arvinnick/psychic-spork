from tests.conftest import MockDatabase, test_now

database = MockDatabase()


#test case: ingredient name is wrong
test_ingredient_name_not_in_database_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat"
                                                            },
                                                  "res_status_code": 400,
                                                  "res_json": {
                                                      'detail': 'ingredient name is not in the database.'
                                                  }
    ,
                                                  "get_db": database.override_db_dependency}


#test case: quantity is zero
test_quantity_zero_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 0.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 422,
                                                  "res_json": {'detail': [{'ctx': {'error': {}},
                                                     'input': {'ingredient': 'Wheat Flour', 'quantity': 0.0},
                                                     'loc': ['body'],
                                                     'msg': 'Assertion failed, Quantity must be positive',
                                                     'type': 'assertion_error'}]}
    ,
                                                  "get_db": database.override_db_dependency}


#test case: quantity is less than zero
test_quantity_negative_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": -1.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 422,
                                                  "res_json": {'detail': [{'ctx': {'error': {}},
             'input': {'ingredient': 'Wheat Flour', 'quantity': -1.0},
             'loc': ['body'],
             'msg': 'Assertion failed, Quantity must be positive',
             'type': 'assertion_error'}]}
    ,
                                                  "get_db": database.override_db_dependency}


#test case: successful creation
test_success_created = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 201,
                                                  "res_json": {'date_time': test_now,
 'ingredient': {'name': 'Wheat Flour',
                'quantity': 500.5,
                'suppliers': [{'address': '1st Valiasr St, Tehran',
                               'email': 'info@tehransupply.com',
                               'name': 'Tehran Supply Co.',
                               'number': 'tel:+98-21-1234-5678'}]},
 'quantity': 1.0}
    ,
                                                  "get_db": database.override_db_dependency}