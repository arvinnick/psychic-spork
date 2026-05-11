from db import models
from db import database


if __name__ == "__main__":
    models.Base.metadata.create_all(database.engine)