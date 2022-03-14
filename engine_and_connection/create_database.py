from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import ForeignKey

meta = MetaData()
engine = create_engine('mysql+pymysql://vidya:Vidya1899@localhost/test', echo=True)


user = Table('user', meta,
             Column('user_id', Integer, primary_key=True),
             Column('name', String(16), nullable=False),
             Column('email_address', String(60)),
             Column('lastname', String(50), nullable=False)
             )

user_prefs = Table('user_prefs', meta,
                   Column('pref_id', Integer, primary_key=True),
                   Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),
                   Column('pref_name', String(40), nullable=False),
                   Column('pref_value', String(100))
                   )


if __name__ == '__main__':
    meta.create_all(engine, checkfirst=True)
    conn = engine.connect()

    # Insert row
    ins = user.insert().values(name='prudhvi', lastname='varma')
    result = conn.execute(ins)

    # Insert rows
    conn.execute(user.insert(), [
        {'name': 'Bhaskar', 'lastname': 'guptha'},
        {'name': 'vibhav', 'lastname': 'kumar'},
        {'name': 'manoj', 'lastname': 'varma'},
    ])
    conn.execute(user_prefs.insert(), [
        {'pref_name': 'Bhas', 'user_id': 1, 'pref_value': 'A'},
        {'pref_name': 'vibh', 'user_id': 2, 'pref_value': 'B'},
        {'pref_name': 'mano', 'user_id': 4,  'pref_value': 'D'},
    ])
    pass

