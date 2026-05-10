from fastapi import APIRouter
from fastapi.params import Depends

from schemas.supplier import SupplierCreate

suppliers_crud_router = APIRouter(
    prefix="/suppliers",
)


@suppliers_crud_router.post('crud')
async def create(supplier: SupplierCreate):#use the dependency for db, make the pydantic schemas first
    """
    endpoint to create a new supplier
    :param supplier: Supplier object
    :return:
    """
    pass
