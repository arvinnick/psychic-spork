from app.db import models
from app.db import database
from sqlalchemy import Engine
from sqlalchemy.exc import DBAPIError

from app.logger import logger


def main(engine: Engine = database.engine):
    try:
        logger.info("initiating the database seeding process...")
        models.Base.metadata.create_all(engine)
        logger.info("database seeded successfully")
    except DBAPIError as e:
        raise e

if __name__ == "__main__":
    main()