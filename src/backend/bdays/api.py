import datetime
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, validator

from bdays import db
from bdays.models import Birthday
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BirthdaySchema(BaseModel):
    id: Optional[int]
    name: str
    surname: Optional[str]
    day: int
    month: int
    year: int

    @classmethod
    def from_object(cls, obj: Birthday):
        return cls(
            id=obj.id, name=obj.name, day=obj.day, month=obj.month, year=obj.year
        )


class PaginationSchema(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = None

    @validator("limit")
    def limit_has_a_limit(cls, limit):
        if limit is None:
            return

        if limit < 0 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        return limit


@app.get("/bday/{bday_id}")
async def get_bday(bday_id: int):
    bday: Birthday = await db.get_bday_by_id(bday_id)
    return BirthdaySchema.from_object(bday)


@app.get("/bdays/list")
async def list_bdays(pagination: Optional[PaginationSchema] = None):
    if pagination is None:
        pagination = {}
    else:
        pagination = pagination.dict()
    return [
        BirthdaySchema.from_object(bday) for bday in await db.list_bdays(**pagination)
    ]


@app.get("/bdays/search")
async def search_bdays(term: str, pagination: Optional[PaginationSchema] = None):
    if pagination is None:
        pagination = {}
    else:
        pagination = pagination.dict()
    return [
        BirthdaySchema.from_object(bday)
        for bday in await db.search_bdays_by_name(term, **pagination)
    ]


@app.post("/bday")
async def create_bday(bday: BirthdaySchema):
    try:
        date = datetime.date(bday.year, bday.month, bday.day)
    except ValueError as ex:
        raise RequestValidationError from ex

    bday = await db.create_bday(
        name=bday.name,
        surname=bday.surname,
        date=date
    )
    return BirthdaySchema.from_object(bday)


@app.delete("/bday/{bday_id}")
async def delete_bday():
    await db.delete_bday_by_id(bday_id)


@app.get("/health")
def ping():
    return {"pong": True}
