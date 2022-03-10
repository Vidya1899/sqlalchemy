from sqlalchemy import create_engine, MetaData

if __name__ == '__main__':
    meta = MetaData()
    engine = create_engine('mysql+pymysql://vidya:Vidya899@localhost/test', echo=True)
    with engine.connect() as conn:
        print("Connection successful")

"""
POSSIBLE ERRORS:
Wrong username: "sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1045, "Access denied for user 
                 'viya'@'localhost' (using password: YES)")"
Wrong password: "sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1045, "Access denied for user 
                 'vidya'@'localhost' (using password: YES)")"
Wrong driver:   "sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:mysql.pmysql"
Wrong dialect:  "sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:myql.pymysql"
Wrong host:     "sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server 
                 on 'localhst' ([Errno 11001] getaddrinfo failed)")"
"""
