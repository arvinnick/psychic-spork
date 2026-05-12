from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase

class Test:
    client = TestClient(app)
    def test_create_inventory_item(self):
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency
        res = self.client.post("/crud/inventory/",
                               json={
                                        "name": "string",
                                        "quantity": 0,
                                        "suppliers": [
                                            "Tehran Supply Co."
                                        ]
                                    })
        assert res.status_code == 200, str(res.json())
        assert res.json() == {'name': 'string',
                              'quantity': 0,
                              'suppliers': [
                                  {
                                      'name': 'Tehran Supply Co.',
                                      'address': '1st Valiasr St, Tehran',
                                      'number': '02112345678',
                                      'email': 'info@tehransupply.com'
                                  }
                              ]
                              }
        app.dependency_overrides = {}







