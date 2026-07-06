from typing import Callable, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base as BaseDBModel
from app.core import config
from app.core.logger import logger
from app.db.models import Orders
from app.db.retrievers import retrieve_orders
from app.internals.helpers import datetime_converter


async def check_if_item_exists(db:AsyncSession,
                              item_id: List[int]|int|None,
                              model:BaseDBModel,
                              getter_func:Callable) -> bool:
    # check if it exists
    try:
        objects = await getter_func(db,
                                    item_id)

        if not objects:
            return False
        else:
            return True

    except Exception as e:
        if isinstance(e, HTTPException):
            if e.status_code == 404:
                raise e
            else:
                pass
        logger.error(
            f"error in deleting {model.name} object, checking for existence: {e}"
        )
        raise HTTPException(
            500, "something went wrong and we don't know what it is:("
        )


async def update_service_layer(item_id:int,
                               existence_checker:callable,
                               db:AsyncSession,
                               db_layer_callable:callable,
                               form_data:dict,
                               first_item:bool=True
                               ):
    logger.info("common method for updating in service layer is called")
    try:
        logger.info(f"existence_checker: {existence_checker.__name__}")
        existence = await existence_checker(db=db, item_id=item_id)
    except HTTPException as he:
        logger.error(f"error in updating loss object: {he}")
        raise he
    except Exception as e:
        logger.error(f"error in updating loss object: {e}")
        raise e
    if existence:
        try:
            form_data["date_time"] = datetime_converter(
                form_data.get("date_time")
            )
            logger.info(f"db_layer_callable: {db_layer_callable.__name__}")
            #
            updated_loss = await db_layer_callable(
                db, item_id, form_data, first_item, existence
            )
        except HTTPException as he:
            logger.error(f"error in updating loss object: {he}")
            raise he
        except Exception as e:
            logger.error(f"error in updating loss object: {e}")
            raise e
        return updated_loss
    else:
        return None


async def get_orders(db:AsyncSession,
                    order_id:List[int]|None = None,
                    ingredient_id:List[int]|None = None,
                    supplier_id:List[int]|None = None,
                    date_time_from:str=None,
                    date_time_to:str=None,
                    quantity_lt:float=None,
                    quantity_gt:float=None,) -> List[Orders]:

    logger.info("Getting order by the specified constraints")
    try:
        if date_time_from:
            date_time_from = datetime_converter(date_time_from)
        if date_time_to:
            date_time_to = datetime_converter(date_time_to)
        db_item = await retrieve_orders(db,
                                                order_id,
                                                ingredient_id,
                                                supplier_id,
                                                date_time_from,
                                                date_time_to,
                                                quantity_lt,
                                                quantity_gt
                                                )
        return db_item
    except Exception as e:
        logger.error(f"service layer, getting orders, has encountered an error: {e}")
        if isinstance(e, HTTPException) and e.status_code in [400, 422]:
            raise e
        elif isinstance(e, ValueError):
            if any(
                [date_time_from in e.args[0], date_time_to in e.args[0] ]
            ):
                raise HTTPException(422, detail=e.args[0])
        else:
            raise HTTPException(status_code=500,
                                detail=str(e) if config.settings.DEBUG else "we got an error on the server. we know no more:(")
