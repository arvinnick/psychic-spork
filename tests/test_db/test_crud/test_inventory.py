from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase

class Test:
    client = TestClient(app)

    def blueprint(self, req_url, req_json, res_status_code, res_json):
        """
        this is a blueprint for the testcases, assuming that most of them are just going to send a request to the server,
        then check the status code and response payload.
        :param req_url: url to send the request to
        :param req_json: request payload in json format
        :param res_status_code: response status code
        :param res_json: response payload in json format
        :return:
        """
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency
        res = self.client.post(req_url, json=req_json)
        assert res.status_code == res_status_code, str(res.json())
        assert res.json() == res_json
        app.dependency_overrides = {}

    def test_create_inventory_item_successful(self):
        # Test successful creation of a new inventory item with valid data and existing suppliers.
        self.blueprint(req_url="/crud/inventory/",
                       req_json={
                                        "name": "string",
                                        "quantity": 0,
                                        "suppliers": [
                                            "Tehran Supply Co."
                                        ]
                                    },
                       res_status_code=201,
                       res_json={'name': 'string',
                              'quantity': 0,
                              'suppliers': [
                                  {
                                      'name': 'Tehran Supply Co.',
                                      'address': '1st Valiasr St, Tehran',
                                      'number': '02112345678',
                                      'email': 'info@tehransupply.com'
                                  }
                              ]
                              })



        app.dependency_overrides = {}
    def test_create_inventory_item_fail(self):
        # TODO: Test creation fails (400/404) when trying to link a supplier name/ID that does not exist.
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency

    # TODO: Test creation with an empty supplier list (if business logic allows it, should succeed; if not, should fail).
    # TODO: Test creation fails (422) when passing a negative quantity (e.g., -10.5).
    # TODO: Test creation behavior with a zero quantity (0.0) - should it succeed or fail?
    # TODO: Test creation fails (422) when required fields (like 'name') are missing from the payload.
    # TODO: Test creation of a duplicate inventory name (e.g., "White Sugar" again) - should it throw a 400 or update the existing one?
    # TODO: Test successful creation linking multiple valid suppliers at once.







