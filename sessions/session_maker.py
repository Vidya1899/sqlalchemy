from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

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
    engine = create_engine('mysql+pymysql://vidya:Vidya1899@localhost/test1', echo=True)
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)

    user = User(name="Vidya", fullname="VidyaGanesh")
    address = Address(email_address="gvidya1899@gmail.com", user_id=1)

    session1 = Session()
    print("session1:", id(session1))
    session1.add(user)
    session1.commit()

    session2 = Session()
    print("session2:", id(session2))
    session2.add(address)
    session2.commit()


