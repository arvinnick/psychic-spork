from fastapi.testclient import TestClient
from app.db.database import get_db
from app.main import app


class Test:
    client = TestClient(app)

    # ==========================================
    # UNIT TESTS FOR SUPPLIER CREATION (POST)
    # ==========================================

    # --- 1. SUCCESS (HAPPY PATH) SCENARIOS ---

    # TODO: Test successful creation with ALL fields provided (name, address, number, email).
    # TODO: Test successful creation with ONLY required fields (name, number) - address and email should default to None.

    # --- 2. VALIDATION FAILURE SCENARIOS (Pydantic 422 Errors) ---

    # TODO: Test creation fails when a required field is missing (e.g., missing 'name').
    # TODO: Test creation fails when a required field is missing (e.g., missing 'number').
    # TODO: Test creation fails with an invalid email format (e.g., "invalid-email.com" without the @ symbol).
    # TODO: Test creation fails with empty strings for required fields (e.g., "name": "").
    # TODO: Test creation behavior with additional unexpected fields (e.g., sending "is_admin": true). Does Pydantic ignore it or forbid it?

    # --- 3. DATABASE LIMIT SCENARIOS (Boundary Testing) ---

    # TODO: Test creation fails when 'name' exceeds 50 characters (String(50) limit).
    # TODO: Test creation fails when 'number' exceeds 15 characters (String(15) limit).

    # --- 4. BUSINESS LOGIC SCENARIOS (400/409 Errors) ---

    # TODO: Test creation fails (400/409) when trying to create a duplicate Supplier Name (Requires checking the DB first or adding unique=True).
    # TODO: Test creation fails (400/409) when trying to create a duplicate Supplier Email or Number (if your business logic requires these to be unique).
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
