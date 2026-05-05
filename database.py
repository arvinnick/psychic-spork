from sqlalchemy import create_engine


'''
test environment
'''
sqlite_file_name = ":memory:" #"restaurant.sqlite"
test_engine = create_engine(f"sqlite+pysqlite:///{sqlite_file_name}", echo=True)


'''
production
'''
#todo:make a postgresql for it
prod_engine = None


#

