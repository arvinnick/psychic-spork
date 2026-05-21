import pytest

from tests.conftest import blueprint_fixture
from tests.test_db.test_crud.parameters.supplier import (test_create_supplier_phone_number_wrong_fail,
                                                         test_create_supplier_success,
                                                         test_create_supplier_wrong_email_format_fail,
                                                         test_create_supplier_no_contact_fail
                                                       )


@pytest.mark.parametrize(
"param_dict",
    [
        test_create_supplier_phone_number_wrong_fail,
        test_create_supplier_success,
        test_create_supplier_wrong_email_format_fail,
        test_create_supplier_no_contact_fail
    ]
)
def test_orders(blueprint_fixture, param_dict):
    blueprint_fixture(param_dict)


def test_ground_truth_test():
    #this is a test to make sure the CICD is working
    assert False