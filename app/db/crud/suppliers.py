from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database import get_db
from schemas.supplier import SupplierCreate

suppliers_crud_router = APIRouter(
    prefix="/suppliers",
)


@suppliers_crud_router.post('/crud')
async def create(supplier: SupplierCreate, db: Annotated[Session, Depends(get_db)]):#use the dependency for db, make the pydantic schemas first
    """
    endpoint to create a new supplier
    :param db: dependency of the database
    :param supplier: Supplier object
    :return:
    """
    try:
        db.add(supplier)
        db.commit()
        return JSONResponse(content=supplier.name, status_code=201)
    except Exception as e:
        return JSONResponse(content=e.args, status_code=400)


