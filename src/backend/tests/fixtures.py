from bdays.db import connect_db

import pytest


@pytest.fixture(scope="function")
async def backend(pg, event_loop):
    pg_user, pg_password = pg
    dsn = f"postgres://postgres:@{pg_user}:{pg_password}/guillotina?sslmode=disable"

    async with connect_db(dsn):
        yield dsn
