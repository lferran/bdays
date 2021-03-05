import pytest
from fastapi.testclient import TestClient

from bdays.api import app
from bdays.db import connect_db


@pytest.fixture(scope="function")
def db():
    import pytest_docker_fixtures

    host, port = pytest_docker_fixtures.pg_image.run()
    yield host, port
    pytest_docker_fixtures.pg_image.stop()


@pytest.fixture(scope="function")
async def backend(db):
    host, port = db
    dsn = f"postgres://postgres:@{host}:{port}/guillotina?sslmode=disable"
    async with connect_db(dsn):
        yield dsn


@pytest.fixture(scope="function")
def client(backend):
    client = TestClient(app)
    yield client
