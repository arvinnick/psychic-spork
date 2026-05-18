from tests.conftest import MockDatabase

database = MockDatabase()

test_create_inventory_item_successful = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "name": "string",
        "quantity": 1,
        "suppliers": [
            "Tehran Supply Co."
        ]
    },
    "res_status_code": 201,
    'res_json': {'name': 'string',
                 'quantity': 1,
                 'suppliers': [
                     {
                         'name': 'Tehran Supply Co.',
                         'address': '1st Valiasr St, Tehran',
                         'number': '02112345678',
                         'email': 'info@tehransupply.com'
                     }
                 ]
                 },
"get_db":database.override_db_dependency
}
test_create_inventory_item_wrong_supplier_fail = {"req_url": "/crud/inventory/",
                                                  "req_json": {
                                                      "name": "string",
                                                      "quantity": 0,
                                                      "suppliers": [
                                                          "Tehran Supply Co.mn"
                                                      ]
                                                  },
                                                  "res_status_code": 400,
                                                  "res_json": {
                                                      'detail': 'Supplier names are not in the database. You need to add themfirst or use the correct id.'
                                                  }
    ,
                                                  "get_db": database.override_db_dependency}
test_create_inventory_item_no_supplier_fail = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "name": "string",
        "quantity": 0,
        "suppliers": []
    },
    "res_status_code": 400,
    "res_json": {
        'detail': 'You must define at least one supplier for an ingredient'
    }
,
                 "get_db":database.override_db_dependency}
test_create_inventory_item_negative_quantity_fail = {"req_url": "/crud/inventory/",
                                                     "res_json": {
                                                         'detail': [
                                                             {
                                                                 'type': 'assertion_error',
                                                                 'loc': ['body'],
                                                                 'msg': 'Assertion failed, '
                                                                        'Inventory quantity must be positive float number',
                                                                 'input': {
                                                                     'name': 'string',
                                                                     'quantity': -1,
                                                                     'suppliers': ['Tehran Supply Co.']},
                                                                 'ctx': {'error': {}}}]},
                                                     "res_status_code": 422,
                                                     "req_json": {
                                                         "name": "string",
                                                         "quantity": -1,
                                                         "suppliers": [
                                                             "Tehran Supply Co."
                                                         ]
                                                     }
    ,
                                                     "get_db": database.override_db_dependency}
test_create_inventory_item_zero_quantity = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "name": "string",
        "quantity": 0,
        "suppliers": [
            "Tehran Supply Co."
        ]
    },
    "res_json": {'name': 'string',
                 'quantity': 0,
                 'suppliers': [
                     {
                         'name': 'Tehran Supply Co.',
                         'address': '1st Valiasr St, Tehran',
                         'number': '02112345678',
                         'email': 'info@tehransupply.com'
                     }
                 ]
                 },
    "res_status_code": 201
,
                 "get_db":database.override_db_dependency}
test_create_inventory_item_missing_name_fail = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "quantity": 1,
        "suppliers": [
            "Tehran Supply Co."
        ]
    },
    "res_status_code": 422,
    "res_json": {
        'detail': [
            {
                'type': 'missing',
                'loc': [
                    'body',
                    'name'
                ],
                'msg': 'Field required',
                'input': {
                    'quantity': 1,
                    'suppliers': [
                        'Tehran Supply Co.'
                    ]
                }
            }
        ]
    }
,
                 "get_db":database.override_db_dependency}
test_duplicate_inventory_name_fail = {
    "req_url": "/crud/inventory/",
    "req_json": {

        "name": "White Sugar",
        "quantity": 1,
        "suppliers": [
            "Tehran Supply Co."
        ]

    },
    "res_status_code": 409,
    "res_json": {
        'detail': 'An inventory item with White Sugar already exists.'
    }
,
                 "get_db":database.override_db_dependency}
test_multiple_suppliers_success = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "name": "string",
        "quantity": 1,
        "suppliers": [
            "Tehran Supply Co.",
            "South Trading"
        ]
    },
    "res_status_code": 201,
    "res_json": {'name': 'string',
                 'quantity': 1,
                 'suppliers': [
                     {
                         'name': 'Tehran Supply Co.',
                         'address': '1st Valiasr St, Tehran',
                         'number': '02112345678',
                         'email': 'info@tehransupply.com'
                     },
                     {
                         "name": "South Trading",
                         "address": "Coastal Blvd, Bandar Abbas",
                         "number": "07612345678",
                         "email": None
                     }

                 ]
                 }
,
                 "get_db":database.override_db_dependency}
