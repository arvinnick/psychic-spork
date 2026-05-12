from db import models
from db import database
from sqlalchemy import Engine


def main(engine: Engine = database.engine):
    models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()