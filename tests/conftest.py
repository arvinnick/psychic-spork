"""
Hardcoded stuff for the tests
"""
import os.path

from httpx import ASGITransport, AsyncClient

from core.config import settings
from datetime import datetime
import pytest
from sqlalchemy import StaticPool
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.models import Inventory, Supplier, SupplierInventoryAssociation, Orders, Losses, Base
from app.main import app
from app.db.database import get_db


async def seed_db(engine, model_base = Base):
    if os.path.exists(engine.url.database):
        os.remove(engine.url.database)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(model_base.metadata.create_all)
    except Exception as e:
        raise e


async def async_session_maker(engine):
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Prevent lazy loading issues after commit
    )




class MockDatabase:
    def __init__(self):
        self.__TEST_DB_ENGINE = settings.TEST_ENGINE_URI
        self.__mock_db_data = {
            "Inventory": [
                {"id": 1, "name": "Wheat Flour", "quantity": 500.5},
                {"id": 2, "name": "White Sugar", "quantity": 200.0},
                {"id": 3, "name": "Vegetable Oil", "quantity": 150.75},
                {"id": 4, "name": "Peanut", "quantity": 150.75}

            ],

            "Supplier": [
                {
                    "id": 1,
                    "name": "Tehran Supply Co.",
                    "address": "1st Valiasr St, Tehran",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                },
                {
                    "id": 2,
                    "name": "South Trading",
                    "address": "Coastal Blvd, Bandar Abbas",
                    "number": 'tel:+98-76-1234-5678',
                    "email": None
                },
                {
                    "id": 3,
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Mashahad",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
                },
                {
                    "id": 4,
                    "name": "Sepehr Machinery",
                    "address": "1st Valiasr St, Tehran",
                    "number": 'tel:+98-21-1234-5678',
                    "email": "info@tehransupply.com"
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


    async def setup(self):
        self.__test_engine = create_async_engine(
            self.__TEST_DB_ENGINE,
            echo=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool  # This keeps the in-memory DB alive!

        )
        await seed_db(self.__test_engine)
        try:
            await self.__seed_test_db()
        except DBAPIError:
            raise Exception("there is a problem in test database seeding")
        except Exception as e:
            if settings.DEBUG:
                raise e
            else:
                raise Exception("tests did not pass")



    async def __seed_test_db(self):
        session = await self.override_get_db()
        for item in self.__mock_db_data["Inventory"]:
            session.add(Inventory(**item))

        for supplier in self.__mock_db_data["Supplier"]:
            session.add(Supplier(**supplier))

        # await session.commit()
        async with self.__test_engine.begin() as conn:
            await conn.execute(
            SupplierInventoryAssociation.insert(),
            self.__mock_db_data["SupplierInventoryAssociation"]
        )

        for loss in self.__mock_db_data["Losses"]:
            session.add(Losses(**loss))

        for order in self.__mock_db_data["Orders"]:
            session.add(Orders(**order))
        await session.commit()

    async def teardown(self):
        # We will call this safely after the tests are done
        app.dependency_overrides.clear()
        await self.__test_engine.dispose()

    async def override_get_db(self) -> AsyncSession:
        """
        Provides a session that automatically begins a transaction.
        Useful when you need explicit transaction boundaries.
        """
        session = await async_session_maker(self.__test_engine)
        return session()



test_now = "2026-05-20T15:40:22"




@pytest.fixture()
async def blueprint_fixture():
    mock_db = MockDatabase()
    await mock_db.setup()
    app.dependency_overrides[get_db] = mock_db.override_get_db
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        async def blueprint(param_dict,
                      client = ac):
            """
            this is a blueprint for the testcases, assuming that most of them are just going to send a request to the server,
            then check the status code and response payload.
            """
            req_url = param_dict["req_url"]
            req_json = param_dict["req_json"]
            res_status_code = param_dict["res_status_code"]
            res_json = param_dict["res_json"]
            response = await client.post(req_url, json=req_json)
            assert response.status_code == res_status_code, str(response.json())
            assert response.json() == res_json
        yield blueprint
        await mock_db.teardown()
        app.dependency_overrides.clear()
