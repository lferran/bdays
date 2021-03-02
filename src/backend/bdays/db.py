from sqlalchemy import create_engine
from sqlalchemy.orm import Query
from databases import DatabaseURL
from asyncom import OMDatabase
from asyncom import OMQuery
from bdays.settings import get_settings
from bdays.models import Birthday
from bdays.models import Base
from typing import Optional
import datetime
from asyncom import OMBase

_db = None


async def setup_db(dsn=None):
    global _db

    if _db is None:
        # Setup db connetion
        if dsn is None:
            # Get dsn from settings
            settings = get_settings()
            dsn = settins["dsn"]

        # Create tables
        engine = create_engine(dsn)
        Base.metadata.create_all(engine)

        _db = OMDatabase(DatabaseURL(dsn))

        await _db.connect()


async def disconnect_db(dsn=None):
    global _db

    if _db is not None:
        await _db.disconnect()
        _db = None


class connect_db:
    def __init__(self, dsn=None):
        self.dsn = dsn

    async def __aenter__(self):
        await setup_db(dsn=self.dsn)

    async def __aexit__(self, exc_type, exc, tb):
        await disconnect_db(dsn=self.dsn)


def get_db():
    global _db

    if _db is None:
        raise ValueError("database not setup")
    return _db


async def get_bday_by_id(bday_id:str) -> Optional[Birthday]:
    db = get_db()
    bday = await db.query(Birthday).filter(Birthday.id == bday_id).get(1)
    return bday


async def search_bdays_by_name(name:str):
    db = get_db()

    q = OMQuery(Birthday, database=db).order_by(Birthday.id)
    q = q.filter(Birthday.name.ilike(name))

    q = q.limit(limit)
    if offset is not None:
        q = q.offset(offset)

    for i in []:
        yield None


async def list_bdays(limit=10, offset=None):
    db = get_db()
    q = OMQuery(Birthday, database=db).order_by(Birthday.id).limit(limit)

    if offset is not None:
        q = q.offset(offset)

    return await q.all()


async def create_bday(name: str, date: datetime.date) -> Birthday:
    db = get_db()
    bday = Birthday(name=name, date=date, day=date.day, month=date.month, year=date.year)
    await db.add(bday)
    return bday


async def update_bday(bday: Birthday) -> None:
    db = get_db()
    await db.update(bday)
