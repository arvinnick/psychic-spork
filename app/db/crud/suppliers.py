from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from db.database import get_db
from db.models import Supplier
from schemas.supplier import SupplierCreate
from schemas.supplier import SupplierBase as SupplierSchema

suppliers_crud_router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)


@suppliers_crud_router.post('/', response_model=SupplierSchema, summary="Create a new supplier entity in the DB")
async def create_supplier(supplier: SupplierCreate, db: Annotated[Session, Depends(get_db)]):
    """
    Endpoint to create a new supplier entity in the database. The supplier is the business which will fullfill
    an order.
    """
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

