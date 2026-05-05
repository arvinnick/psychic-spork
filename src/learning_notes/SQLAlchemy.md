# SQLAlchemy

- We have ORM and Core in SQLAlchemy.  
- Connection, engine and session definitions:  
  - Engine: It holds a pool of open connections to the database. We don’t open and close the connections repeatedly because it’s an expensive task.  
  - Connection: an open connection from the engine’s pool  
  - Session: some of the data from database on the RAM, which could be committed.  
- Engine is a global object by which we connect to the database. We make it using the “create\_engine” function.  
- The create\_engine function takes a string argument as well as “echo”, which is a boolean argument about logging.  
- Engine provides a session/connection object to connect to the database. Session is for ORM and Connection is for core.  
- Session will open a resource, so it is better to be used by the python context manager. After the context is closed, the transactions will be rolled back. But no change will be made on the database unless you commit it. There is also an autocommit mode.  
- The method “begin” of the engine will open the context, then roll it back or commit it based on if the transaction was successful or it had an exception.  
- Connection has an execute method. It returns a “result” object. This object has many methods, including “all” which gives all the rows. It is also iterable for rows. Rows are like name tuples.  
- Use bond parameters for execution. These are the parameters of the SQL statements.  
- You can just say with session(engine) instead of with engine.connect() as conn  
- Session.commit is only necessary for a situation in which we are changing the database (not for SELECT, for example).  
- Committing a session will expire it, meaning that the system will no longer trust it. To make it trustworthy, we should use session.refresh() method.  
- Database metadata: python objects that represent tables, columns and other data which describes the data. Here are these objects:  
  - Table: the representation of a relation. They can be constructed using ORM, Table class in core or from an existing database, which is called a reflection. This obj will assign itself to a Metadata obj.   
  - Metadata: a facade (?) around a dictionary which will hold table objects as well as their string names. Metadata is a reflection of a database but it can be only reflecting to a part of it. Having a single MD obj for the entire application is the most common use. Metadata object has a “create\_all” method which emits all its relations to the database (just the create statements), doing everything in order. Also, “drop\_all” will emit drop statements in reverse order.  
  - Column: A DB col. Will be assigned to a table obj. Columns of a table are accessible via table\_obj.c  
  - Integer, String: a value in a database, will be assigned to a column even without instantiation.

### Table reflection

making Table and related objects using the current state of the database. To do that we can make a plain metadata and a plain table object and use the “autoload\_with” parameter for the table, passing the target “engine”.

## ORM:

The declarative table is a process by which we make a table, which is a reflection of the database relations. During this process we get an ORM mapped class as well. 

* Mapped class is any class in Python that its attributes are linked to database table columns  
* Metadata is associated with DeclarativeBase in ORM. It is accessible via DeclarativeBase.Metadata. So you can use the create\_all or drop\_all methods of it.  
* The registry is also accessible via DeclarativeBase.registery. It is a set of Python objects representing tables and their relations, to be used in ORM.  
* The DeclarativeBase is not the only way to map; but the most common one. The ORM supports Python dataclasses for mapping as well.
