from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from app.db.database import get_db
from app.db.models import Supplier
from app.core.logger import logger
from app.db.retrievers import retrieve_suppliers_by_id


async def db_layer_retrieve_supplier(db:Annotated[AsyncSession, Depends(get_db)],
                                     supplier_id: int = None) -> List[Supplier]:
    logger.info("Getting order by the specified constraints")
    suppliers = await retrieve_suppliers_by_id(
        db=db, supplier_id=supplier_id
    )
    return suppliers