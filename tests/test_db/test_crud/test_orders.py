from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase


class Test:
    client = TestClient(app)
    def test_create(self):
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency
        res = self.client.post("/crud/orders/",
                               json={
                                   "quantity": 1,
                                   "ingredient": "Wheat Flour",
                                   "supplier": "Tehran Supply Co."
                               }) #simple post req
        assert res.status_code == 200
        assert res.json() == {'ingredient': {'name': 'Wheat Flour',
                'quantity': 500.5,
                'suppliers': [{'address': '1st Valiasr St, Tehran',
                               'email': 'info@tehransupply.com',
                               'name': 'Tehran Supply Co.',
                               'number': '02112345678'}]},
 'quantity': 1.0,
 'supplier': {'address': '1st Valiasr St, Tehran',
              'email': 'info@tehransupply.com',
              'name': 'Tehran Supply Co.',
              'number': '02112345678'}}
        # failed_res = self.client.post("/suppliers/crud",data={'name': ''})
        app.dependency_overrides = {}
