from bdays.db import connect_db
from bdays.db import get_db
from bdays.models import Base
from bdays.models import Birthday
from sqlalchemy import create_engine
import pytest
from sqlalchemy import delete
from fastapi.testclient import TestClient
from bdays.api import app


async def delete_test_data(dsn):
    """this doesn't work right now..."""
    db = get_db()
    # Delete all test data after every test
    engine = create_engine(dsn)
    meta = Base.metadata
    for tbl in reversed(meta.sorted_tables):
        # engine.execute(tbl.delete())
        stmt = (
            delete(tbl).
            where(True)
        )
        await db.execute(stmt)


class empty_test_db(connect_db):
    async def __aexit__(self, exc_type, exc, tb):
        # TODO: need to figure out a way to clean the bdays table at
        # the end of every test so that there is no garbage data
        # across tests.
        await delete_test_data(self.dsn)
        await super().__aexit__(exc_type, exc, tb)


@pytest.fixture(scope="function")
async def backend(pg):
    pg_user, pg_password = pg
    dsn = f"postgres://postgres:@{pg_user}:{pg_password}/guillotina?sslmode=disable"

    async with empty_test_db(dsn):
        yield dsn


@pytest.fixture(scope="function")
def client(backend):
    client = TestClient(app)
    yield client
