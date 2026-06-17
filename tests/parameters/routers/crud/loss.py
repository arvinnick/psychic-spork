from tests.conftest import frozen_test_time


##############post
#test case: ingredient name is wrong
test_ingredient_name_not_in_database_fail = {"req_url": "/crud/losses",
                                                  "req_json": {
                                                                "quantity": 1.0,
                                                                "ingredient": "Wheat"
                                                            },
                                                  "res_status_code": 400,
                                                  "res_json": {'detail': 'ingredient name is not in the database.'}
                                             }


#test case: quantity is zero
test_quantity_zero_fail = {"req_url": "/crud/losses",
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
test_quantity_negative_fail = {"req_url": "/crud/losses",
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
test_success_created = {"req_url": "/crud/losses",
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








##############get
test_success_all = {
    "req_url": "/crud/losses",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-25T14:30:00",
                    "ingredient_id": 1,
                    "quantity": 5.0
                },
                {
                    "date_time": "2023-10-26T09:15:00",
                    "ingredient_id": 2,
                    "quantity": 2.5
                }
            ]
                        }

test_success_singular = {
    "req_url": "/crud/losses/1",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-25T14:30:00",
                    "ingredient_id": 1,
                    "quantity": 5.0
                }
            ]
}

test_fail_string_id = {
    "req_url": "/crud/losses/a",
    "method": "get",
    "res_status_code": 400,
    "res_json":
                {"details":"Invalid ID format. ID should be an integer."}
}

test_success_singular_id_non_existent = {
    "req_url": "/crud/losses/4",
    "method": "get",
    "res_status_code": 200,
    "res_json": []
}

test_success_singular_ingredient = {
    "req_url": "/crud/losses/1/ingredient",
    "method": "get",
    "res_status_code": 200,
    "res_json":  {"name": "Wheat Flour", "quantity": 500.5},
}

test_fail_wrong_sub_resources = {
    "req_url": "/crud/losses/1/something_else",
    "method": "get",
    "res_status_code": 400,
    "res_json":  {
        "details": "loss endpoint does not support 'something_else' as a sub-resource."
    },
}

test_filter_ingredient_id = {
    "req_url": "/crud/losses?ingredient_id=1",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-25T14:30:00",
                    "ingredient_id": 1,
                    "quantity": 5.0
                }
            ]
}

test_filter_ingredient_id_wrong_format = {
    "req_url": "/crud/losses?ingredient_id=something",
    "method": "get",
    "res_status_code": 422,
    "res_json": {'detail': [{'input': 'something',
             'loc': ['query', 'ingredient_id', 0],
             'msg': 'Input should be a valid integer, unable to parse string '
                    'as an integer',
             'type': 'int_parsing'}]}
}

test_filter_datetime_to = {
    "req_url": "/crud/losses?datetime_to=2023-10-25T20:30:00",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-25T14:30:00",
                    "ingredient_id": 1,
                    "quantity": 5.0
                }
            ]
}

test_filter_datetime_from = {
    "req_url": "/crud/losses?datetime_from=2023-10-25T20:30:00",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-26T09:15:00",
                    "ingredient_id": 2,
                    "quantity": 2.5
                }
            ]
}


test_filter_datetime_from_to = {
    "req_url": "/crud/losses?datetime_to=2023-10-30T20:30:00&datetime_from=2023-10-25T20:30:00",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-26T09:15:00",
                    "ingredient_id": 2,
                    "quantity": 2.5
                }
            ]
}

test_filter_datetime_to_wrong_format = {
    "req_url": "/crud/losses?datetime_to=1",
    "method": "get",
    "res_status_code": 422,
    "res_json":
                {
                    "detail": "Invalid isoformat string: '1'"
                }

}

test_filter_quantity_gt = {
    "req_url": "/crud/losses?quantity_gt=3",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "date_time": "2023-10-25T14:30:00",
                    "ingredient_id": 1,
                    "quantity": 5.0
                }
            ]
}

test_filter_quantity_lt = {
    "req_url": "/crud/losses?quantity_lt=3",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {
            "date_time": "2023-10-26T09:15:00",
            "ingredient_id": 2,
            "quantity": 2.5
        }
    ]
}

test_filter_quantity_lt_wrong_format = {
    "req_url": "/crud/losses?quantity_lt=a",
    "method": "get",
    "res_status_code": 422,
    "res_json": {
        "detail": [
            {
                "input": "a",
                "loc": ["query", "quantity_lt"],
                "msg": "Input should be a valid number, unable to parse string as "
                "a number",
                "type": "float_parsing",
            }
        ]
    },
}

test_filter_quantity_gt_wrong_format = {
    "req_url": "/crud/losses?quantity_gt=a",
    "method": "get",
    "res_status_code": 422,
    "res_json": {'detail': [{'input': 'a',
             'loc': ['query', 'quantity_gt'],
             'msg': 'Input should be a valid number, unable to parse string as '
                    'a number',
             'type': 'float_parsing'}]},
}


test_filter_quantity_gt_lt = {
    "req_url": "/crud/losses?quantity_gt=2&quantity_lt=3",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {
            "date_time": "2023-10-26T09:15:00",
            "ingredient_id": 2,
            "quantity": 2.5
        }
    ]
}


###delete
test_successful_delete = {
    "req_url": "/crud/losses/1",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":True,
    "res_json": None,
}

test_wrong_format_delete = {
    "req_url": "/crud/losses/asa",
    "method": "delete",
    "res_status_code": 422,
    "existing_resource":False,
    "res_json": {"details":"Invalid ID format. ID should be an integer."},
}

test_non_existing_resource_delete = {
    "req_url": "/crud/losses/5",
    "method": "delete",
    "res_status_code": 404,
    "existing_resource":False,
    "res_json": {"details":"ID doesn't exist."},
}
