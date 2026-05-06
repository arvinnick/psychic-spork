from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.models.base import Base

crudRouter = APIRouter()




def create(model:Base,
           db:Session, ) -> Base:
    """
    create inventory entity and commits it to the database
    :return: created inventory object
    """
    for key, value in kwargs.items():
        if hasattr(model, key):
            setattr(model, key, value)
        else:
            raise AttributeError(f"{key} is not a valid attribute for {model.__tablename__}")
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


