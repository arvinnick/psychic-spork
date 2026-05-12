from datetime import datetime

from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase


class Test():
    client = TestClient(app)
    def test_create(self):
        mock_db = MockDatabase()
        app.dependency_overrides[get_db] = mock_db.override_db_dependency
        time_now = str(datetime.now())
        res = self.client.post("/crud/losses/",
                               json={
                                   "date_time": time_now,
                                   "ingredient": "White Sugar",
                                   "quantity": 2.0
                               }) #simple post req
        assert res.status_code == 200, res.json()
        assert res.json() == {
            'date_time': time_now.replace(' ', 'T'),
            'ingredient': {
                'name': 'White Sugar',
                'quantity': 200,
                'suppliers': [
                    {
                        'name': 'Tehran Supply Co.',
                        'address': '1st Valiasr St, Tehran',
                        'number': '02112345678',
                        'email': 'info@tehransupply.com'
                    }
                ]
            },
            'quantity': 2.0}
        app.dependency_overrides = {}
