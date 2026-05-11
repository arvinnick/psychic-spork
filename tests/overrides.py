"""
Hardcoded stuff for the tests
"""

from datetime import datetime

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

from app.db.models import Inventory, Supplier, SupplierInventoryAssociation, Orders, Losses


class MockDatabase:
    def __init__(self):
        self.__TEST_DB_PATH = ":memory:"  # "restaurant.sqlite"
        self.__TEST_DB_ENGINE = f"sqlite+pysqlite:///{self.__TEST_DB_PATH}"
        self.__test_engine = create_engine(self.__TEST_DB_ENGINE, echo=True)
        self.db = Session(self.__test_engine)
        self.__mock_db_data = {
        "inventory": [
            {"id": 1, "name": "Wheat Flour", "quantity": 500.5},
            {"id": 2, "name": "White Sugar", "quantity": 200.0},
            {"id": 3, "name": "Vegetable Oil", "quantity": 150.75}
        ],

        "supplier": [
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

        "supplier_inventory_association": [
            {"supplier_id": 1, "inventory_id": 1},
            {"supplier_id": 1, "inventory_id": 2},
            {"supplier_id": 2, "inventory_id": 3}
        ],

        "losses": [
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

        "orders": [
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


    def __seed_test_db(self):
        for item in self.__mock_db_data["inventory"]:
            self.db.add(Inventory(**item))

        for supplier in self.__mock_db_data["supplier"]:
            self.db.add(Supplier(**supplier))

        self.db.commit()
        for assoc in self.__mock_db_data["supplier_inventory_association"]:
            stmt = insert(SupplierInventoryAssociation).values(assoc)
            self.db.execute(stmt)

        for loss in self.__mock_db_data["losses"]:
            self.db.add(Losses(**loss))

        for order in self.__mock_db_data["orders"]:
            self.db.add(Orders(**order))

        self.db.commit()

    def override_db_dependency(self):
        self.__seed_test_db()
        try:
            yield self.db
        finally:
            self.db.close()