

#####post
#testcase: no contact is provided
test_create_supplier_no_contact_fail = {
    "req_url": "/crud/suppliers/",
    "req_json": {"name": "Aramco"},
    "res_status_code": 422,
    "res_json":{'detail': [{'ctx': {'error': {}},
             'input': {'name': 'Aramco'},
             'loc': ['body'],
             'msg': 'Value error, you should add at least one of the ways to '
                    'contact the supplier.',
             'type': 'value_error'}]}
}
#test case: the email format is wrong
test_create_supplier_wrong_email_format_fail = {
    "req_url": "/crud/suppliers/",
    "req_json": {
        "name": "Aramco",
        "email": ""},
    "res_status_code": 422,
    "res_json":{
        'detail': [
            {'ctx': {'reason': 'An email address must have an @-sign.'},
             'input': '',
             'loc': ['body', 'email'],
             'msg': 'value is not a valid email address: An email address must '
                    'have an @-sign.',
             'type': 'value_error'}
        ]
    }
}
#test case: the phone number format is wrong with numbers
test_create_supplier_phone_number_wrong_fail = {
    "req_url": "/crud/suppliers/",
    "req_json": {
        "name": "Aramco",
        "email": "info@aram.co",
        "number": "57034727"},
    "res_status_code": 422,
    "res_json":{
        'detail':
                    [
                        {'input': '57034727',
                         'loc': ['body', 'number'],
                         'msg': 'value is not a valid phone number',
                         'type': 'value_error'}
                    ]
    }
}
#test case: successful creation
test_create_supplier_success = {
    "req_url": "/crud/suppliers/",
    "req_json": {
        "name": "Aramco",
        "email": "info@aram.co",
        "number": "+1 650-253-0000",
        "address":"1, Aram road, Riad, Saudi Arabia"},
    "res_status_code": 201,
    "res_json":{

        "name": "Aramco",
        "email": "info@aram.co",
        "number": 'tel:+1-650-253-0000',
        "address":"1, Aram road, Riad, Saudi Arabia"
    }
}

#####get

test_get_all_suppliers_success = {
    "req_url": "/crud/suppliers",
    "method": "get",
    "res_status_code": 200,
    "res_json":[
                {
                    "name": "Tehran Supply Co.",
                    "address": "1st Valiasr St, Tehran",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                },
                {
                    "name": "South Trading",
                    "address": "Coastal Blvd, Bandar Abbas",
                    "number": 'tel:+98-76-1234-5678',
                    "email": None
                },
                {
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Mashahad",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                },
                {
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Tehran",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                }
            ]

}
test_get_single_supplier_success = {
    "req_url": "/crud/suppliers/1",
    "res_status_code": 200,
    "method": "get",
    "res_json": [
        {
            "name": "Tehran Supply Co.",
            "address": "1st Valiasr St, Tehran",
            "number": "tel:+98-21-1234-5678",
            "email": "info@tehransupply.com"
        }
    ],
}
test_get_single_supplier_wrong_format = {
    "req_url": "/crud/suppliers/a",
    "res_status_code": 422,
    "method": "get",
    "res_json": {
        "detail": [
            {
                "input": "a",
                "loc": ["path", "supplier_id"],
                "msg": "Input should be a valid integer, unable to parse string "
                "as an integer",
                "type": "int_parsing",
            }
        ]
    },
}
test_get_supplier_ingredients_success = {
    "req_url": "/crud/suppliers/1/ingredients",
    "res_status_code": 200,
    "method": "get",
    "res_json": [
        {"name": "Wheat Flour", "quantity": 500.5},
        {"name": "White Sugar", "quantity": 200.0},
    ],
}
test_get_supplier_wrong_property = {
    "req_url": "/crud/suppliers/1/something_else",
    "method": "get",
    "res_status_code": 404,
    "res_json": {"detail": "Not Found"},
}
test_get_single_non_existent_supplier_success = {
    "req_url": "/crud/suppliers/54",
    "method": "get",
    "res_status_code": 200,
    "res_json": [],
}


test_case_get_list = {
    "req_url": "/crud/suppliers?supplier_id=3&supplier_id=4",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Mashahad",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                },
                {
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Tehran",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                }
    ],
}


####delete
test_case_successful_delete = {
    "req_url": "/crud/suppliers/3",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":True,
    "res_json": None,
}


test_case_successful_delete_list = {
    "req_url": "/crud/suppliers?supplier_id=3&supplier_id=4",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":True,
    "res_json": None,
}

test_wrong_format_delete = {
    "req_url": "/crud/suppliers/asa",
    "method": "delete",
    "res_status_code": 422,
    "existing_resource":False,
    "res_json": {'detail': [{'input': 'asa',
             'loc': ['path', 'supplier_id'],
             'msg': 'Input should be a valid integer, unable to parse string '
                    'as an integer',
             'type': 'int_parsing'}]},
}

test_non_existing_resource_delete = {
    "req_url": "/crud/suppliers/5",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":False,
    "res_json": {"detail":"ID doesn't exist"},
}

###update

test_case_update_fail_non_existing_supplier = {
    "req_url": "/crud/suppliers/8",
    "req_json": {
        "name": "MammadCo",
        "email": "info@aram.co",
        "number": "57034727"},
    "method": "put",
    "res_status_code": 204,
    "res_json": {"detail":"Supplier doesn't exist"},
}

test_case_update_fail_non_existing_attribute = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name_": "MammadCo",
        "email": "info@aram.co",
        "number": "57034727"},
    "method": "put",
    "res_status_code": 400,
    "res_json": {"detail":"attribute name_ doesn't exist"},
}

test_case_update_success_name = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name": "MammadCo",
        "email": "info@aram.co",
        "number": "tel:+1-650-253-0000"},
    "method": "put",
    "res_status_code": 200,
    "res_json": {
        "name": "MammadCo",
        "email": "info@aram.co",
        "number": "tel:+1-650-253-0000"},
}

test_case_update_success_email = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "tel:+1-650-253-0000"},
    "method": "put",
    "res_status_code": 200,
    "res_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "tel:+1-650-253-0000"},
}

test_case_update_success_phone = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "tel:+1-650-253-0000"},
    "method": "put",
    "res_status_code": 200,
    "res_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "tel:+1-650-253-0000"},
}

test_case_update_fail_phone = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "ds"},
    "method": "put",
    "res_status_code": 422,
    "res_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "ds"},
}

test_case_update_fail_email = {
   "req_url": "/crud/suppliers/1",
    "req_json": {
        "name": "MammadCo",
        "email": "12",
        "number": "tel:+1-650-253-0000"},
    "method": "put",
    "res_status_code": 422,
    "res_json": {
        "name": "MammadCo",
        "email": "info@mammad.co",
        "number": "tel:+1-650-253-0000"},
}