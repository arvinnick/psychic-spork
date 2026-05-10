from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

##TODO: add this into a config file
PROD = False
PROD_ENGINE_URI = ''
TEST_SQLITE_FILE_NAME = "./test_db.sqlite" #"restaurant.sqlite"
TEST_ENGINE_URI = f"sqlite+pysqlite:///{TEST_SQLITE_FILE_NAME}"


if PROD:
    engine = create_engine(PROD_ENGINE_URI, echo=True)
else:
    engine = create_engine(TEST_ENGINE_URI, echo=True)


Session = sessionmaker(bind=engine)


def get_db():
    with Session(bind=engine) as session:
        yield session


if __name__ == "__main__":
    Base.metadata.create_all(engine)