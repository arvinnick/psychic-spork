from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

import app.config as config
from app.logger import logger
from app.db.database import get_db
from app.schemas.losses import Loss as LossesSchema
from app.schemas.losses import LossesCreate
from app.db.models import Losses, Inventory

losses_crud_router = APIRouter(
    prefix="/losses",
    tags=["losses"],
)
logger.info(f"Defined the losses router.")

@losses_crud_router.post('/', response_model=LossesSchema,
                         summary="creating a loss of ingredients record in the database",
                         status_code=201)
def create_loss(loss: LossesCreate, db: Annotated[Session, Depends(get_db)]) -> Losses:
    """
    Creates a loss entity. When an ingredient is thrown away due to spoilage, we use this path operation to record it.
    """
    logger.info(f"Creating a loss of ingredient: {loss.ingredient}")
    try:
        ingredients = db.execute(select(Inventory).where(Inventory.name == loss.ingredient)).scalars().all()
        if not ingredients:
            raise HTTPException(status_code=400, detail="ingredient name is not in the database.")
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
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")