from app.db.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from fastapi import Response

from app.core.logger import logger


async def db_layer_updater(
        model:Base,
        item_id:int,
        form_data:dict,
        db:AsyncSession,
        db_layer_id_checker:callable,
        first_item:bool,
        existence_cache=None):
    logger.info(f"updating {model.__tablename__} on db layer")
    try:
        query = (
            update(model).where(model.id == item_id).returning(model)
        )
        updated_object = await db.execute(query, form_data)
    except IntegrityError as ie:
        if existence_cache is None:
            if not await db_layer_id_checker(db, form_data.get(item_id)):
                return Response(f"{model.__tablename__} ID doesn't exist", 204)
        else:
            if existence_cache:
                raise ie
            else:
                return Response(f"{model.__tablename__} ID doesn't exist", 204)
    except Exception as e:
        logger.error(f"an error in db layer for {model.__tablename__} update: {e}")
        raise e
    try:
        await db.commit()
        if first_item:
            return_value = updated_object.scalars().first()
        else:
            return_value = updated_object.scalars().all()
    except Exception as e:
        logger.error(f"an error in db layer for {model.__tablename__} update: {e}")
        raise e
    return return_value