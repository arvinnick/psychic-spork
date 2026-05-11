from fastapi.testclient import TestClient

from app.db.database import get_db
from app.main import app
from tests.overrides import MockDatabase


class Test:
    client = TestClient(app)
    def test_create(self):
        app.dependency_overrides[get_db] = MockDatabase.override_db_dependency
        self.client.post("/suppliers/crud", json={"supplier": "test"})
        app.dependency_overrides = {}
