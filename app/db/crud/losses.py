from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from schemas.losses import Loss as LossesSchema
from schemas.losses import LossesCreate
from db.models import Losses, Inventory

losses_crud_router = APIRouter(
    prefix="/losses",
)

@losses_crud_router.post('/', response_model=LossesSchema)
def create_loss(loss: LossesCreate, db: Annotated[Session, Depends(get_db)]) -> Losses:
    try:
        ingredients = db.execute(select(Inventory).where(Inventory.name == loss.ingredient)).scalars().all()
        if not ingredients:
            raise HTTPException(status_code=400, detail="ingredient name is not in the database")
        elif len(ingredients) > 1:
            raise HTTPException(status_code=400, detail="ingredient name is not in the database")
        db_item = Losses(
            quantity=loss.quantity,
            date_time=loss.date_time,
            ingredient=ingredients[0]
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))