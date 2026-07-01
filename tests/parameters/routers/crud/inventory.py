
####post
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
                                                  "res_status_code": 404,
                                                  "res_json": {
                                                      'detail': 'Supplier not found in the database.'}
                                                  }
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


####get
test_get_all_inventory = {
    "req_url": "/crud/inventory",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
                {"name": "Wheat Flour", "quantity": 500.5},
                {"name": "White Sugar", "quantity": 200.0},
                {"name": "Vegetable Oil", "quantity": 150.75},
                {"name": "Peanut", "quantity": 150.75},
                {'name': 'Cucumber', 'quantity': 3.75}
    ]
}
test_get_ont_inventory_item = {
    "req_url": "/crud/inventory/1",
    "method": "get",
    "res_status_code": 200,
    "res_json": [{"name": "Wheat Flour", "quantity": 500.5}],
}
test_get_one_inventory_item_suppliers = {
    "req_url": "/crud/inventory/1/suppliers",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
            {
                "address": "1st Valiasr St, Tehran",
                "email": "info@tehransupply.com",
                "name": "Tehran Supply Co.",
                "number": "tel:+98-21-1234-5678",
            }
    ],
}
test_get_wrong_format_inventory_item_fail = {
    "req_url": "/crud/inventory/as",
    "method": "get",
    "res_status_code": 422,
    "res_json": {
                    'detail': [
                        {'input': 'as',
                         'loc': [
                             'path', 'ingredient_id'
                         ],
                         'msg': 'Input should be a valid integer, unable to parse string as an integer',
                         'type': 'int_parsing'
                         }
                    ]
    }
}
test_get_inventory_non_existent_id = {
    "req_url": "/crud/inventory/6",
    "method": "get",
    "res_status_code": 200,
    "res_json": []
}
test_get_inventory_wrong_property = {
    "req_url": "/crud/inventory/1/something",
    "method": "get",
    "res_status_code": 404,
    "res_json": {"detail": "Not Found"},
}
test_get_inventory_filter_suppliers = {
    "req_url": "/crud/inventory?supplier_id=1",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {"name": "Wheat Flour", "quantity": 500.5},
        {"name": "White Sugar", "quantity": 200.0}
    ],
}
test_get_inventory_filter_quantity_from = {
    "req_url": "/crud/inventory?quantity_from=300",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {"name": "Wheat Flour", "quantity": 500.5},
    ]
}
test_get_inventory_filter_quantity_to_from = {
    "req_url": "/crud/inventory?quantity_from=300&quantity_to=500",
    "method": "get",
    "res_status_code": 200,
    "res_json": []
}
test_get_inventory_filter_quantity_to = {
    "req_url": "/crud/inventory?quantity_to=175",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {"name": "Vegetable Oil", "quantity": 150.75},
        {"name": "Peanut", "quantity": 150.75},
        {'name': 'Cucumber', 'quantity': 3.75}
    ],
}
test_get_inventory_filter_quantity_empty = {
    "req_url": "/crud/inventory?quantity_to=100",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {'name': 'Cucumber', 'quantity': 3.75}
    ],
}
test_get_inventory_by_name = {
    "req_url": "/crud/inventory?name=peanut",
    "method": "get",
    "res_status_code": 200,
    "res_json": [
        {"name": "Peanut", "quantity": 150.75}
    ],
}
test_get_inventory_by_name_multiple = {
    "req_url": "/crud/inventory?name=peanut&name=vegetable-oil",
    "method": "get",
    "res_status_code": 200,
    "res_json": [{'name': 'Vegetable Oil', 'quantity': 150.75},
                 {'name': 'Peanut', 'quantity': 150.75}],
}

##delete
test_successful_delete = {
    "req_url": "/crud/inventory/4",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":True,
    "res_json": None,
}

test_successful_delete_list = {
    "req_url": "/crud/inventory?ingredient_id=4&ingredient_id=5",
    "method": "delete",
    "res_status_code": 204,
    "existing_resource":True,
    "res_json": None,
}

test_wrong_format_delete = {
    "req_url": "/crud/inventory/asa",
    "method": "delete",
    "res_status_code": 422,
    "existing_resource":False,
    "res_json": {'detail': [{'input': 'asa',
             'loc': ['path', 'ingredient_id'],
             'msg': 'Input should be a valid integer, unable to parse string '
                    'as an integer',
             'type': 'int_parsing'}]},
}

test_non_existing_resource_delete = {
    "req_url": "/crud/inventory/6",
    "method": "delete",
    "res_status_code": 404,
    "existing_resource":False,
    "res_json": {"detail":"ID doesn't exist"},
}


test_dependant_entity_delete_restrict = {
    "req_url": "/crud/inventory/1",
    "method": "delete",
    "res_status_code": 409,
    "existing_resource":False,
    "res_json": {"detail":"the operation is restricted by database constraints"},
}


####put
#success
test_put_inventory_item_successful_quantity = {
    "req_url": "/crud/inventory/3",
    "method": "put",
    "req_json": {
        "name": "Vegetable Oil",
        "quantity": 200,
        "suppliers": [
           2
        ]
    },
    "res_status_code": 200,
    'res_json': {
        "name": "Vegetable Oil",
        "quantity": 200,
                 },
    "dependent_objects": [
        {
            "req_url": "/crud/suppliers/2/ingredients",
            "res_status_code": 200,
            "method": "get",
            "res_json": [
                {"name": "Vegetable Oil", "quantity": 150.75}
            ]
        }
    ]
}




test_put_inventory_item_successful_name_and_supplier = {
    "req_url": "/crud/inventory/3",
    "method": "put",
    "req_json": {
        "name": "Vegetable Oil",
        "quantity": 2,
        "suppliers": [1],
    },
    "res_status_code": 200,
    "res_json": {
        "name": "Vegetable Oil",
        "quantity": 2,
    },
    "dependent_objects": [
        {
            "req_url": "/crud/suppliers/3/ingredients",
            "res_status_code": 200,
            "method": "get",
            "res_json": [
                {"name": "Vegetable Oil", "quantity": 200}
            ]
        }
    ]
}


#fail
test_put_inventory_item_fail_non_existing_entity = {
    "req_url": "/crud/inventory/8",
    "method": "put",
    "req_json": {
        "name": "updated_string",
        "quantity": 2,
        "suppliers": [2],
    },
    "res_status_code": 204,
    "res_json": {"details": "the inventory item doesn't exist"},
}


test_put_inventory_item_fail_no_suppliers = {
    "req_url": "/crud/inventory/8",
    "method": "put",
    "req_json": {
        "name": "updated_string",
        "quantity": 2,
        "suppliers": [],
    },
    "res_status_code": 400,
    "res_json": {"details": "the inventory item doesn't exist"},
}


test_put_inventory_item_fail_non_existing_attribute = {
    "req_url": "/crud/inventory/1",
    "method": "put",
    "req_json": {
        "namee": "updated_string",
        "quantity": 2,
        "suppliers": [2],
    },
    "res_status_code": 422,
    "res_json": {'detail': [{'input': {'namee': 'updated_string',
                       'quantity': 2,
                       'suppliers': [2]},
             'loc': ['body', 'name'],
             'msg': 'Field required',
             'type': 'missing'}]},
}

test_put_inventory_item_fail_validation = {
    "req_url": "/crud/inventory/1",
    "method": "put",
    "req_json": {
        "namee": "updated_string",
        "quantity": -1,
        "suppliers": [2],
    },
    "res_status_code": 422,
    "res_json": {'detail': [{'input': {'namee': 'updated_string',
                       'quantity': -1,
                       'suppliers': [2]},
             'loc': ['body', 'name'],
             'msg': 'Field required',
             'type': 'missing'},
            {'ctx': {'ge': 0.0},
             'input': -1,
             'loc': ['body', 'quantity'],
             'msg': 'Input should be greater than or equal to 0',
             'type': 'greater_than_equal'}]},
}

test_put_inventory_item_fail_type = {
    "req_url": "/crud/inventory/1",
    "method": "put",
    "req_json": {
        "namee": "updated_string",
        "quantity": "asa",
        "suppliers": [2],
    },
    "res_status_code": 422,
    "res_json": {'detail': [{'input': {'namee': 'updated_string',
                       'quantity': 'asa',
                       'suppliers': [2]},
             'loc': ['body', 'name'],
             'msg': 'Field required',
             'type': 'missing'},
            {'input': 'asa',
             'loc': ['body', 'quantity'],
             'msg': 'Input should be a valid number, unable to parse string as '
                    'a number',
             'type': 'float_parsing'}]},
}

