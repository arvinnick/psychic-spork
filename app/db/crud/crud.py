from fastapi import APIRouter

from .inventory import inventory_crud_router

crud_router = APIRouter(
    prefix="/crud",
)
crud_router.include_router(inventory_crud_router)





