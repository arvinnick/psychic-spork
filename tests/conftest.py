"""
Hardcoded stuff for the tests
"""

from datetime import datetime
import pytest
from sqlalchemy import create_engine, insert, StaticPool
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.db.models import Inventory, Supplier, SupplierInventoryAssociation, Orders, Losses
from app.main import app
import seed_db
from app.db.database import get_db

class MockDatabase:
    def __init__(self):
        self.__TEST_DB_PATH = ":memory:"  # "restaurant.sqlite"
        self.__TEST_DB_ENGINE = f"sqlite+pysqlite:///{self.__TEST_DB_PATH}"
        self.__test_engine = create_engine(
            self.__TEST_DB_ENGINE,
            echo=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool  # This keeps the in-memory DB alive!
        )
        seed_db.main(self.__test_engine)
        self.db = Session(self.__test_engine)
        self.__mock_db_data = {
        "Inventory": [
            {"id": 1, "name": "Wheat Flour", "quantity": 500.5},
            {"id": 2, "name": "White Sugar", "quantity": 200.0},
            {"id": 3, "name": "Vegetable Oil", "quantity": 150.75}
        ],

        "Supplier": [
            {
                "id": 1,
                "name": "Tehran Supply Co.",
                "address": "1st Valiasr St, Tehran",
                "number": "02112345678",
                "email": "info@tehransupply.com"
            },
            {
                "id": 2,
                "name": "South Trading",
                "address": "Coastal Blvd, Bandar Abbas",
                "number": "07612345678",
                "email": None
            }
        ],

        "SupplierInventoryAssociation": [
            {"supplier_id": 1, "inventory_id": 1},
            {"supplier_id": 1, "inventory_id": 2},
            {"supplier_id": 2, "inventory_id": 3}
        ],

        "Losses": [
            {
                "id": 1,
                "date_time": datetime(2023, 10, 25, 14, 30, 0),
                "ingredient_id": 1,
                "quantity": 5.0
            },
            {
                "id": 2,
                "date_time": datetime(2023, 10, 26, 9, 15, 0),
                "ingredient_id": 2,
                "quantity": 2.5
            }
        ],

        "Orders": [
            {
                "id": 1,
                "date_time": datetime(2023, 11, 1, 10, 0, 0),
                "quantity": 100.0,
                "ingredient_id": 1,
                "supplier_id": 1
            },
            {
                "id": 2,
                "date_time": datetime(2023, 11, 5, 11, 45, 0),
                "quantity": 50.0,
                "ingredient_id": 3,
                "supplier_id": 2
            }
        ]
    }
        self.__seed_test_db()


    def __seed_test_db(self):
        for item in self.__mock_db_data["Inventory"]:
            self.db.add(Inventory(**item))

        for supplier in self.__mock_db_data["Supplier"]:
            self.db.add(Supplier(**supplier))

        self.db.commit()
        for assoc in self.__mock_db_data["SupplierInventoryAssociation"]:
            stmt = insert(SupplierInventoryAssociation).values(assoc)
            self.db.execute(stmt)

        for loss in self.__mock_db_data["Losses"]:
            self.db.add(Losses(**loss))

        for order in self.__mock_db_data["Orders"]:
            self.db.add(Orders(**order))

        self.db.commit()

    def override_db_dependency(self):
        try:
            yield self.db
        finally:
            pass



@pytest.fixture()
def blueprint_fixture():
    mock_db = MockDatabase()
    app.dependency_overrides[get_db] = mock_db.override_db_dependency
    test_client = TestClient(app)
    def blueprint(param_dict,
                  client = test_client):
        """
        this is a blueprint for the testcases, assuming that most of them are just going to send a request to the server,
        then check the status code and response payload.
        """
        req_url = param_dict["req_url"]
        req_json = param_dict["req_json"]
        res_status_code = param_dict["res_status_code"]
        res_json = param_dict["res_json"]
        res = client.post(req_url, json=req_json)
        assert res.status_code == res_status_code, str(res.json())
        assert res.json() == res_json
    yield blueprint
    app.dependency_overrides = {}


