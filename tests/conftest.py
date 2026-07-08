"""
Hardcoded stuff for the tests
"""
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.db.database import get_db, get_engine
from app.main import app
from tests.mock_database import MockDatabase

frozen_test_time = "2026-05-20T15:40:22"



@pytest_asyncio.fixture()
async def db_instance():
    db_instance = MockDatabase()
    await db_instance.setup()
    db = await db_instance.override_get_db()
    yield db
    await db_instance.teardown()



@pytest_asyncio.fixture(scope="class")
async def blueprint_fixture():
    mock_db = MockDatabase()
    await mock_db.setup()
    app.dependency_overrides[get_db] = mock_db.override_get_db
    app.dependency_overrides[get_engine] = mock_db.override_get_engine
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        async def blueprint(param_dict,
                      client = ac):
            """
            this is a blueprint for the testcases, assuming that most of them are just going to send a request to the server,
            then check the status code and response payload.
            """
            async def ingred_association_commons():
                # step2:send the request
                if param_dict.get("method") == "post":
                    response = await ac.post(param_dict.get("request_endpoint"))  # param3
                elif param_dict.get("method") == "delete":
                    response = await ac.delete(param_dict.get("request_endpoint"))  # param3
                else:
                    raise ValueError(f"the method should be delete or put. It is {param_dict.get("method")}")
                # step3:make sure the status code is 200
                assert response.status_code == param_dict.get("response_status_code")  # param4
                supposed_response_load = param_dict.get("response_payload")
                if supposed_response_load:
                    assert response.json() == supposed_response_load
            if param_dict.get("supplier_ingredient_relation", False):
                if param_dict.get("success"):
                    # success #param1
                    # step1:get the orders and store them
                    if param_dict.get("orders_check"):
                        orders = await ac.get("/crud/orders")  # param2
                    await ingred_association_commons()
                    # step4:get the supplier for the ingredient
                    suppliers = await ac.get(param_dict.get("child_checking_endpoint"))  # param5
                    # step5:make sure the get method for dependent suppliers contains the new one
                    suppliers_objects = suppliers.json()
                    assert all(suppused_supplier_obj in suppliers_objects for suppused_supplier_obj in param_dict.get(
                        "child_check_response_payload"))  # json is param6
                    if param_dict.get("orders_check"):
                        # step6:make sure the orders are not affected
                        updated_orders = await ac.get("/crud/orders")
                        assert orders.json() == updated_orders.json()
                else:
                    await ingred_association_commons()
            else:
                req_url = param_dict["req_url"]
                req_json = param_dict.get("req_json")
                res_status_code = param_dict["res_status_code"]
                res_json = param_dict["res_json"]
                method = param_dict.get("method", "post")
                dependent_objects =  param_dict.get("dependent_objects")
                if method == "post":
                    response = await client.post(req_url, json=req_json)
                elif method == "put":
                    response = await client.put(req_url, json=req_json)
                elif method == "delete":
                    response = await client.delete(req_url)
                elif method == "patch":
                    response = await client.patch(req_url, json=req_json)
                elif method == "get":
                    response = await client.get(req_url)
                else:
                    raise ValueError("Invalid HTTP method specified in the test case.")
                assert response.status_code == res_status_code, str(response.json())
                if res_status_code != 204:
                    assert response.json() == res_json
                if param_dict.get("existing_resource"):
                    if method == "delete":
                        check_deleted_resource = await client.get(req_url)
                        try:
                            assert check_deleted_resource.json() == []
                        except AssertionError:
                            raise AssertionError("the resources are not deleted")
                    elif method == "put":
                        if dependent_objects:
                            for dependent_object in dependent_objects:
                                await blueprint(param_dict=dependent_object)

        yield blueprint
        await mock_db.teardown()
        app.dependency_overrides.clear()


