from tests.conftest import frozen_test_time
from app.core.config import settings

DEBUG = settings.DEBUG



#test case: ingredient name is wrong
test_ingredient_name_not_in_database_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat"
                                                            },
                                                  "res_status_code": 404 if DEBUG else 500,
                                                  "res_json": {
                                                      'detail': 'Ingredient not found in the database.' if DEBUG else "The server has encountered an error"
                                                  }
                                             }


#test case: quantity is zero
test_quantity_zero_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 0.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 422,
                                                  "res_json": {'detail': [{'ctx': {'gt': 0.0},
             'input': 0.0,
             'loc': ['body', 'quantity'],
             'msg': 'Input should be greater than 0',
             'type': 'greater_than'}]}
                           }


#test case: quantity is less than zero
test_quantity_negative_fail = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": -1.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 422,
                                                  "res_json": {'detail': [{'ctx': {'gt': 0.0},
             'input': -1.0,
             'loc': ['body', 'quantity'],
             'msg': 'Input should be greater than 0',
             'type': 'greater_than'}]}
                               }


#test case: successful creation
test_success_created = {"req_url": "/crud/losses/",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat Flour"
                                                            },
                                                  "res_status_code": 201,
                                                  "res_json": {'date_time': frozen_test_time,
 'ingredient': {'name': 'Wheat Flour',
                'quantity': 500.5,
                'suppliers': [{'address': '1st Valiasr St, Tehran',
                               'email': 'info@tehransupply.com',
                               'name': 'Tehran Supply Co.',
                               'number': 'tel:+98-21-1234-5678'}]},
 'quantity': 1.0}
                        }