# Sessions

**session** establishes all conversations with the database and represents a “holding zone” for all the objects which you’ve loaded or associated with it during its lifespan

**sessionmaker** provides a factory for Session objects with a fixed configuration. As it is typical that an application will have an Engine object in module scope, the sessionmaker can provide a factory for Session objects that are against this engine.

**scoped_session** :  scoped_session object represents a registry of Session objects.


Reference: https://docs.sqlalchemy.org/en/14/orm/session_basics.html

# Session Management

**Transient** - An instance that’s not in a session, and is not saved to the database; i.e. it has no database identity.

**Pending** - When you Session.add() a transient instance, it becomes pending (not flushed to the database yet).

**Persistent** - An instance which is present in the session and has a record in the database.

**Deleted** - An instance which has been deleted within a flush, but the transaction has not yet completed. 

**Detached** - An instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session.

Reference: https://docs.sqlalchemy.org/en/14/orm/session_state_management.html
