from tests.conftest import MockDatabase
database = MockDatabase()


#testcase: no contact is provided
test_create_supplier_no_contact_fail = {
    "req_url": "/crud/suppliers/",
    "req_json": {"name": "Aramco"},
    "res_status_code": 422,
    "res_json":{'detail': 'you should add at least one of the ways to contact the supplier.'},
"get_db":database.override_db_dependency
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
    },
"get_db":database.override_db_dependency
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
    },
"get_db":database.override_db_dependency
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
    },
"get_db":database.override_db_dependency
}

