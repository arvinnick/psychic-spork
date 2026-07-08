from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from core.logger import logger
from db.crud.inventory import database_layer_add_supplier_to_ingredient
from db.injectors import database_layer_add_ingredient_to_supplier
from services.inventory import check_if_ingredient_id_exists
from services.supplier import (
    check_if_supplier_id_exists,
)


async def service_layer_add_ingredient_to_supplier(db:AsyncSession, engine:AsyncEngine,
                                                   ingredient_id:List[int]|int, supplier_id:int):
    logger.info(f"adding ingredient id {ingredient_id} to the supplier id {supplier_id} in the service layer")
    try:
        (
            values_to_be_added,
            ingredient_cache,
            supplier_cache,
        ) = await supplier_ingredient_update_values_provider(db=db,
                                                             supplier_id=supplier_id, ingredient_id=ingredient_id,
                                                             multiple_suppliers=False)
        updated_combination = await database_layer_add_ingredient_to_supplier(engine=engine,
                                                                              supplier_id=supplier_id,
                                                                              values_to_be_added=values_to_be_added,)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in adding supplier to the ingredient, service layer: {e}")
        raise e
    return updated_combination


async def service_layer_add_supplier_to_ingredient(db:AsyncSession, engine:AsyncEngine,
                                                   ingredient_id:int, supplier_id:List[int]|int):
    logger.info(f"adding supplier id {supplier_id} to the ingredient id {ingredient_id} in the service layer")
    try:
        (values_to_be_added,
         ingredient_cache,
         supplier_cache) = await supplier_ingredient_update_values_provider(db=db,
                                                                            supplier_id=supplier_id,
                                                                            ingredient_id=ingredient_id)
        updated_combination = await database_layer_add_supplier_to_ingredient(engine=engine,
                                                                              ingredient_id=ingredient_id,
                                                                              values_to_be_added=values_to_be_added)
    except HTTPException as he:
        logger.error(he)
        raise he
    except Exception as e:
        logger.error(f"error in adding supplier to the ingredient, service layer: {e}")
        raise e
    return updated_combination


async def supplier_ingredient_update_values_provider(db:AsyncSession,
                                                     supplier_id:int|List[int],
                                                     ingredient_id:int|List[int],
                                                     multiple_suppliers:bool=True):
    ingredient_cache, ingredient_existence = await check_if_ingredient_id_exists(db=db,
                                                                                 ingredient_id=ingredient_id)
    if not ingredient_existence:
        logger.error(f"ingredient id {ingredient_id} does not exist")
        raise HTTPException(status_code=406, detail=f"ingredient id {ingredient_id} does not exist")
    supplier_cache, supplier_existence = await check_if_supplier_id_exists(db=db,
                                                                           supplier_id=supplier_id)
    if not supplier_existence:
        logger.error(f"one or more supplier ids {supplier_id} do not exist")
        raise HTTPException(status_code=406, detail=f"one or more supplier ids {supplier_id} do not exist")
    if multiple_suppliers:
        if isinstance(supplier_id, list):
            values_to_be_added = [(ingredient_id, supp_id) for supp_id in supplier_id]
        else:
            values_to_be_added = [(ingredient_id, supplier_id)]
    else:
        if isinstance(ingredient_id, list):
            values_to_be_added = [(ingred_id, supplier_id) for ingred_id in ingredient_id]
        else:
            values_to_be_added = [(ingredient_id, supplier_id)]
    return values_to_be_added, ingredient_cache, supplier_cache
