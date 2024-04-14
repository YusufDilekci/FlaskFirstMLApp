from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session


url = URL.create(
    drivername="postgresql",
    username="postgres",
    database="FlaskAppDB",
    password=1234
)

engine = create_engine(url)

engine.connect()
Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    fname = Column(String(250), nullable=False)
    lname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    comment = Column(String(250), nullable=False)


Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


