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


@suppliers_crud_router.post('/', response_model=SupplierSchema)
async def create_supplier(supplier: SupplierCreate, db: Annotated[Session, Depends(get_db)]):
    """
    endpoint to create a new supplier
    :param db: dependency of the database
    :param supplier: Supplier object
    :return:
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

