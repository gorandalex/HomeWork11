from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    phone = Column(String, index=True, nullable=False)
    birthday = Column(Date, index=True, nullable=False)
    description = Column(String)

