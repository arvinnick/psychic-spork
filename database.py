from sqlalchemy import create_engine
from sqlalchemy.orm import Session

'''
test environment
'''
sqlite_file_name = "restaurant.sqlite"
test_engine = create_engine(f"sqlite:///{sqlite_file_name}")
session = Session(test_engine)


'''
production
'''
#todo:make a postgresql for it
prod_engine = None


#

