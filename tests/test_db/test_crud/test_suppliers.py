from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase


class Test:
    client = TestClient(app)
    def test_create(self):
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency
        res = self.client.post("/crud/suppliers/", json={
                'name': 'mamal',
                'address': 'alllll',
                'number': '0930',
                'email': 'a@gmail.com'
        }) #simple post req
        assert res.status_code == 200
        assert res.json() == {
                'name': 'mamal',
                'address': 'alllll',
                'number': '0930',
                'email': 'a@gmail.com'
        }
        # failed_res = self.client.post("/suppliers/crud",data={'name': ''})
        app.dependency_overrides = {}
