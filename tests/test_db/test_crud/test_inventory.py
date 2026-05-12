from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase

class Test:
    client = TestClient(app)
    def test_create_inventory_item(self):
        app.dependency_overrides[get_db] = MockDatabase.override_db_dependency
        res = self.client.post("/suppliers/crud",
                               json={
                                        "name": "string",
                                        "quantity": 0,
                                        "suppliers": [
                                            1
                                        ]

                                    })
        assert res.status_code == 200
        assert res.json() == {
                                "name": "string",
                                "quantity": 0,
                                "suppliers": [
                                    1
                                ]

                            }
        app.dependency_overrides = {}







