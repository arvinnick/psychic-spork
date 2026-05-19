from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.db.models import Supplier
from app.logger import logger
from app.schemas.supplier import SupplierCreate
from app.schemas.supplier import SupplierBase as SupplierSchema

suppliers_crud_router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)
logger.info(f"Defined the suppliers router.")


@suppliers_crud_router.post('/',
                            response_model=SupplierSchema,
                            summary="Create a new supplier entity in the DB")
async def create_supplier(supplier: SupplierCreate, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to create a new supplier entity in the database. The supplier is the business which will fullfill
    an order.
    """
    logger.info(f"Creating a new supplier with name: {supplier.name}")
    try:
        db_item = Supplier(
            **supplier.model_dump()
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

