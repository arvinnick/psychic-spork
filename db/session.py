from sqlalchemy import create_engine

##TODO: add this into a config file
PROD = False
PROD_ENGINE_URI = ''
TEST_SQLITE_FILE_NAME = ":memory:" #"restaurant.sqlite"
TEST_ENGINE_URI = f"sqlite+pysqlite:///{TEST_SQLITE_FILE_NAME}"


if PROD:
    engine = create_engine(PROD_ENGINE_URI, echo=True)
else:
    engine = create_engine(TEST_ENGINE_URI, echo=True)