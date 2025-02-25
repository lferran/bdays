import datetime

import pytest

from bdays.db import (
    create_bday,
    get_bday_by_id,
    list_bdays,
    search_bdays_by_name,
    update_bday,
)

pytestmark = pytest.mark.asyncio


async def test_get_birthday(backend):
    date = datetime.date(1991, 11, 12)
    bday = await create_bday(name="Foo", date=date)

    bday = await get_bday_by_id(bday.id)
    assert bday.id == 1
    assert bday.name == "Foo"
    assert bday.date == date
    assert bday.day == date.day
    assert bday.month == date.month
    assert bday.year == date.year

    # Check that if id is not found, returns None
    assert await get_bday_by_id(12314) is None


async def test_create_birthday(backend):
    date = datetime.date(1991, 11, 12)
    bday = await create_bday(name="Foo", date=date)
    assert bday.id == 1
    assert bday.name == "Foo"
    assert bday.date == date
    assert bday.day == date.day
    assert bday.month == date.month
    assert bday.year == date.year


async def test_update_birthday(backend):
    date = datetime.date(1991, 11, 12)
    bday = await create_bday(name="Foo", date=date)

    bday.name = "Bar"
    await update_bday(bday)

    # Check it was updated
    bday = await get_bday_by_id(bday.id)
    assert bday.name == "Bar"


async def test_list_birthdays(backend):
    for i in range(10):
        date = datetime.date(1991, 11, 12)
        await create_bday(name=f"Foo{i}", date=date)

    page = await list_bdays()
    assert len(page) == 10

    # Check sorting order
    ids = [bd.id for bd in page]
    assert ids == list(range(1, 11))


async def test_list_birthdays_pagination(backend):
    for i in range(20):
        date = datetime.date(1991, 11, 12)
        await create_bday(name=f"Foo{i}", date=date)

    page = await list_bdays(limit=5, offset=0)
    assert len(page) == 5

    second_page = await list_bdays(limit=5, offset=5)
    assert len(second_page) == 5

    ids = [bd.id for bd in page + second_page]
    assert ids == list(range(1, 11))


async def test_search_by_name(backend):
    date = datetime.date(1991, 11, 12)
    await create_bday(name="John", surname="Doe", date=date)

    for term in ("john", "doe", "JoHn DoE", "DoE"):
        results = await search_bdays_by_name(term)
        assert len(results) > 0
