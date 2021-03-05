from asyncom import OMBase
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=OMBase)


class Birthday(Base):
    __tablename__ = "bdays"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    def __repr__(self):
        display_name = self.name
        if self.surname:
            display_name += f" {self.surname}"
        return f"<Birthday(name={display_name}, date={self.date})>"
