from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.db.models import Base
from app.core.logger import logger



async def deleter(db: AsyncSession,
                   model: Base,
                   id:int|List[int]) -> Base|List[Base]:
    logger.info(f"deleting {id} from {model.__tablename__}")
    if isinstance(id, int):
        query = delete(model).where(model.id == id).returning(model.id)
    else:
        query = delete(model).where(model.id.in_(id)).returning(model.id)
    try:
        result = await db.execute(query)
        return result.scalars().all()
    except IntegrityError as ie:
        logger.error(ie)
        raise HTTPException(status_code=409, detail="the operation is restricted by database constraints")
    except Exception as e:
        logger.error(f"error in retrieving database object for deleting: {e}")
        raise HTTPException(status_code=500, detail="there is a problem in the server and we don't know whtat it is:(")