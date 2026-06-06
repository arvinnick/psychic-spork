from fastapi import APIRouter

from app.routers.crud.inventory import inventory_crud_router
from app.routers.crud.losses import losses_crud_router
from app.routers.crud.orders import orders_crud_router
from app.routers.crud.suppliers import suppliers_crud_router
from app.core.logger import logger

crud_router = APIRouter(
    prefix="/crud",
    tags=["crud operations"],
)
logger.info("Defined the crud router.")
crud_router.include_router(inventory_crud_router)
logger.info("Added the inventory router.")

crud_router.include_router(suppliers_crud_router)
logger.info("Added the suppliers router.")
crud_router.include_router(losses_crud_router)
logger.info("Added the losses router.")
crud_router.include_router(orders_crud_router)
logger.info("Added the orders router.")





