import datetime
from typing import Optional

from asyncom import OMBase, OMDatabase, OMQuery
from databases import DatabaseURL
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Query

from bdays.models import Base, Birthday
from bdays.settings import get_settings

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


async def get_bday_by_id(bday_id: str) -> Optional[Birthday]:
    db = get_db()
    bday = await db.query(Birthday).filter(Birthday.id == bday_id).get(1)
    return bday


async def search_bdays_by_name(search_term: str, limit=10, offset=None):
    db = get_db()
    q = OMQuery(Birthday, database=db).order_by(Birthday.id)
    or_terms = []
    for term in search_term.split(" ")[:5]:  # up to 5 terms
        term = term.lower().rstrip().lstrip()
        or_terms.extend(
            [Birthday.name.ilike(f"%{term}%"), Birthday.surname.ilike(f"%{term}%")]
        )
    q = q.filter(or_(*or_terms))
    q = q.limit(limit)
    if offset is not None:
        q = q.offset(offset)
    return await q.all()


async def list_bdays(limit=10, offset=None):
    db = get_db()
    q = OMQuery(Birthday, database=db).order_by(Birthday.id).limit(limit)

    if offset is not None:
        q = q.offset(offset)

    return await q.all()


async def create_bday(name: str, date: datetime.date, surname=None) -> Birthday:
    db = get_db()
    bday = Birthday(
        name=name,
        surname=surname,
        date=date,
        day=date.day,
        month=date.month,
        year=date.year,
    )
    await db.add(bday)
    return bday


async def update_bday(bday: Birthday) -> None:
    db = get_db()
    await db.update(bday)
