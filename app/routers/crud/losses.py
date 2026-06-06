from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import app.core.config as config
from app.core.logger import logger
from app.db.database import get_db
from app.schemas.losses import Loss as LossesSchema, LossesRead
from app.schemas.losses import LossesCreate
from app.db.models import Losses
from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_inventory

losses_crud_router = APIRouter(
    prefix="/losses",
    tags=["losses"],
)
logger.info("Defined the losses router.")

@losses_crud_router.post('/', response_model=LossesSchema,
                         summary="creating a loss of ingredients record in the database",
                         status_code=201)
async def create_loss(loss: LossesCreate,
                      db: Annotated[AsyncSession, Depends(get_db)],
                      ) -> Losses:
    """
    Creates a loss entity. When an ingredient is thrown away due to spoilage, we use this path operation to record it.
    """
    logger.info(f"Creating a loss of ingredient: {loss.ingredient}")
    try:
        ingredients = await retrieve_inventory(loss.ingredient, db)
        if not ingredients:
            raise HTTPException(status_code=400, detail="ingredient name is not in the database.")
        db_item = Losses(
            quantity=loss.quantity,
            date_time=loss.date_time,
            ingredient=ingredients
        )
        await db_item_injector(db_item, db)
        return db_item
    except HTTPException as he:
        if he.status_code in [400, 404]:
            raise he
        else:
            raise HTTPException(
                status_code=500, detail="The server has encountered an error"
            )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")


@losses_crud_router.get('/', response_model=List[LossesRead], status_code=200,
                        summary="reading and filtering the recorded losses")
async def get_losses(loss:LossesRead, db:Annotated[AsyncSession, Depends(get_db)]):
    """
    main path operation for reading the losses. you can filter the losses by ingredient name, date_time, and quantity.
     if you don't provide any query parameters, it will return all the losses.
    """
    logger.info(f"Getting losses by the parameters provided: {loss}")
    try:
        query = select(Losses)
        if loss.ingredient:
            query = query.filter(Losses.ingredient == loss.ingredient)
        if loss.date_time:
            query = query.filter(Losses.date_time == loss.date_time)
        if loss.quantity:
            query = query.filter(Losses.quantity == loss.quantity)
        db_items = await db.execute(query).scalars().all()
        return db_items
    except Exception as e:
        raise e