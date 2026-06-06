from IPython.core.magics import config

from app.core import config

DEBUG = config.settings.DEBUG

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
                         'number': 'tel:+98-21-1234-5678',
                         'email': 'info@tehransupply.com'
                     }
                 ]
                 }
}
test_create_inventory_item_wrong_supplier_fail = {"req_url": "/crud/inventory/",
                                                  "req_json": {
                                                      "name": "string",
                                                      "quantity": 0,
                                                      "suppliers": [
                                                          "Tehran Supply Co.mn"
                                                      ]
                                                  },
                                                  "res_status_code": 404 if DEBUG else 500,
                                                  "res_json": {
                                                      'detail': 'Supplier not found in the database.' if DEBUG else "we got an error on the server. we know no more:("}
                                                  }

test_create_inventory_item_no_supplier_fail = {
    "req_url": "/crud/inventory/",
    "req_json": {
        "name": "string",
        "quantity": 0,
        "suppliers": []
    },
    "res_status_code": 400 if DEBUG else 500,
    "res_json": {
        'detail': 'You must define at least one supplier for an ingredient' if DEBUG else "we got an error on the server. we know no more:("
    }
}
test_create_inventory_item_negative_quantity_fail = {"req_url": "/crud/inventory/",
                                                     "res_json": {
                                                         'detail': [{'ctx': {'ge': 0.0},
             'input': -1,
             'loc': ['body', 'quantity'],
             'msg': 'Input should be greater than or equal to 0',
             'type': 'greater_than_equal'}]
                                                         ,


    },
                                                     "req_json": {
                                                         "name": "string",
                                                         "quantity": -1,
                                                         "suppliers": [
                                                             "Tehran Supply Co."
                                                         ]
                                                     },
                                                     "res_status_code": 422
                                                     }
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
                         'number': 'tel:+98-21-1234-5678',
                         'email': 'info@tehransupply.com'
                     }
                 ]
                 },
    "res_status_code": 201

}
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
}
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
        'detail': 'An inventory item with the name White Sugar already exists.'
    }
}
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
                         'number': 'tel:+98-21-1234-5678',
                         'email': 'info@tehransupply.com'
                     },
                     {
                         "name": "South Trading",
                         "address": "Coastal Blvd, Bandar Abbas",
                         "number": "tel:+98-76-1234-5678",
                         "email": None
                     }

                 ]
                 }
}
