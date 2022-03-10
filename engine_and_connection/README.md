## Engine and Connection

### Database Urls
The **create_engine()** function produces an Engine object based on a URL. These URLs can include username, password, hostname, database name as well as optional keyword arguments for additional configuration. In some cases a file path is accepted, and in others a “data source name” replaces the “host” and “database” portions. The typical form of a database URL is:

```
dialect+driver://username:password@host:port/database
```

The **MySQL** dialect uses **mysql-python** as the default **DBAPI**. There are many MySQL DBAPIs available, including MySQL-connector-python and OurSQL:

#### Default
```
engine = create_engine('mysql://vidya:Vidya1899@localhost/test')
```

#### mysqlclient (a maintained fork of MySQL-Python)
```
engine = create_engine('mysql+mysqldb://vidya:Vidya1899@localhost/test')
```

#### PyMySQL
```
engine = create_engine('mysql+pymysql://vidya:Vidya1899@localhost/test')
```

Reference : [sqlalchemy engines (Official Docs)](https://docs.sqlalchemy.org/en/14/core/engines.html)
