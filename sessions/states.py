from sqlalchemy.orm import declarative_base
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, ForeignKey, inspect
from sqlalchemy.orm import Session, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(20))
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


if __name__ == '__main__':
    engine = db.create_engine('mysql+pymysql://vidya:Vidya1899@localhost/test1', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)

    user = User(name="Vidya", fullname="VidyaGanesh")
    insp = inspect(user)
    print("@@ State is Transient:", insp.transient)

    session1 = Session()

    session1.add(user)
    insp = inspect(user)
    print("@@ State is Pending:", insp.pending)

    session1.commit()
    insp = inspect(user)
    print("@@ State is Persistent:", insp.persistent)

    session1.expunge(user)
    insp = inspect(user)
    print("@@ State is Detached:", insp.detached)

    session2 = Session()
    addr = Address(email_address="gvidya1899@gmail.com", user_id=1)
    session2.add(addr)
    session2.commit()


