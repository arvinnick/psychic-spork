from fastapi import APIRouter

from app.db.crud.inventory import inventory_crud_router
from app.db.crud.losses import losses_crud_router
from app.db.crud.orders import orders_crud_router
from app.db.crud.suppliers import suppliers_crud_router
from app.logger import logger

crud_router = APIRouter(
    prefix="/crud",
    tags=["crud operations"],
)
logger.info(f"Defined the crud router.")
crud_router.include_router(inventory_crud_router)
logger.info(f"Added the inventory router.")

crud_router.include_router(suppliers_crud_router)
logger.info(f"Added the suppliers router.")
crud_router.include_router(losses_crud_router)
logger.info(f"Added the losses router.")
crud_router.include_router(orders_crud_router)
logger.info(f"Added the orders router.")





