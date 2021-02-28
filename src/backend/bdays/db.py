from sqlalchemy import Base
from sqlalchemy import create_engine


dbsession = None


def get_db():
    if dbsession is None:
        dsn = "todo"
        engine = create_engine(dsn)
        Base.metadata.create_all(engine)
        dbsession = OMDatabase(DatabaseURL(dsn))
    return dbsession


async def get_bday_by_id(bday_id:str):
    return {}


async def search_bdays_by_name(name:str):
    for i in []:
        yield None


async def list_bdays(size=10, offset=None):
    for i in []:
        yield None


async def create_bday(bday: Birthday) -> Birthday:
    db = get_db()
    await db.add(bday)
    return bday

async def update_bday(bday: Birthday) -> Birthday:
    db = get_db()
    await db.update(bday)
    return bday
