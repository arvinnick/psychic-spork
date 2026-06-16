from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.config as config
from app.core.logger import logger
from app.db.database import get_db
from app.schemas.losses import Loss as LossesSchema, LossGet
from app.schemas.losses import LossesCreate
from app.schemas.inventory import InventoryBase as InventorySchema
from app.db.models import Losses, Inventory
from app.db.injectors import db_item_injector
from app.db.retrievers import retrieve_inventory
from app.services.losses import get_losses
from services.inventory import get_ingredients

losses_crud_router = APIRouter(
    prefix="/losses",
    tags=["losses"],
)
logger.info("Defined the losses router.")

@losses_crud_router.post('', response_model=LossesSchema,
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
        ingredients = await get_ingredients(db=db,
                                            ingredient_name=loss.ingredient,
                                            first_item=True)

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
        logger.error(f"error in creating loss endpoint: {e}")
        raise HTTPException(status_code=500,
                            detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")


@losses_crud_router.get('/{loss_id}',
                        response_model=LossGet,
                        status_code=200,
                        summary="reading a single recorded loss by id")
async def get_single_loss(db:Annotated[AsyncSession, Depends(get_db)],
                          loss_id: int
                     ) -> List[Losses]:
    """
    main path operation for reading the losses. you can filter the losses by ingredient name, date_time, and quantity.
     if you don't provide any query parameters, it will return all the losses.
    """
    logger.info("Getting losses by ID")
    try:
        loss_objects = await get_losses(db, [loss_id])
        return loss_objects
    except Exception as e:
        logger.error(f"error in getting losses endpoint: {e}")
        raise HTTPException(500,
                            "something went wrong and we don't know what it is:(")


@losses_crud_router.get('',
                        response_model=LossGet,
                        status_code=200,
                        summary="reading loss records based on the constraints and filters")
async def get_losses_path_operation(db:Annotated[AsyncSession, Depends(get_db)],
                                    loss_id: Annotated[List[int], int | None, Query()] = None,
                                    ingredient_id: Annotated[List[int], int | None, Query()] = None,
                                    datetime_to: str | None = None,
                                    datetime_from: str | None = None,
                                    quantity_lt: float | None = None,
                                    quantity_gt: float | None = None,
                     ) -> List[Losses]:
    """
    main path operation for reading the losses. you can filter the losses by ingredient name, date_time, and quantity.
     if you don't provide any query parameters, it will return all the losses.
    """
    logger.info("Getting losses by constraints")
    try:
        loss_objects = await get_losses(db,
                                        loss_id,
                                        ingredient_id,
                                        datetime_to,
                                        datetime_from,
                                        quantity_lt,
                                        quantity_gt)
        return loss_objects
    except HTTPException as he:
        logger.error(f"validation error in getting losses endpoint: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in getting losses endpoint: {e}")
        raise HTTPException(500,
                            "something went wrong and we don't know what it is:(")




@losses_crud_router.get('/{loss_id}/ingredient',
                        response_model=InventorySchema,
                        status_code=200,
                        summary="reading loss records based on the constraints and filters")
async def get_losses_ingredient(db:Annotated[AsyncSession, Depends(get_db)],
                                loss_id: int
                                ) -> Inventory:
    """
    main path operation for reading the losses. you can filter the losses by ingredient name, date_time, and quantity.
     if you don't provide any query parameters, it will return all the losses.
    """
    logger.info("Getting losses by constraints")
    try:
        loss_objects = await get_losses(db,
                                        loss_id)
        return loss_objects[0].ingredient
    except Exception as e:
        logger.error(f"error in getting losses endpoint: {e}")
        raise HTTPException(500,
                            "something went wrong and we don't know what it is:(")