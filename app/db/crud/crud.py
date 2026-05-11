from fastapi import APIRouter

from db.crud.inventory import inventory_crud_router
from db.crud.suppliers import suppliers_crud_router

crud_router = APIRouter(
    prefix="/crud",
)
crud_router.include_router(inventory_crud_router)
crud_router.include_router(suppliers_crud_router)





