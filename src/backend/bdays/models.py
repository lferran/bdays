from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class Birthday(Base):
    __tablename__ = 'bdays'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(Date)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    def __repr__(self):
        return f"<Birthday(name={self.name}, date={self.date})>"
