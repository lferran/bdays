from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import validator
from typing import Optional
from bdays import db
from bdays.models import Birthday

app = FastAPI()


class BirthdayType(BaseModel):
    id: Optional[str]
    name: str
    day: int
    month: int
    year: int

    @classmethod
    def from_object(cls, obj: Birthday):
        return cls(
            id=obj.id,
            name=obj.name,
            day=obj.day,
            month=obj.month,
            year=obj.year
        )


class PaginationSchema(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = None

    @validator('limit')
    def limit_has_a_limit(cls, limit):
        if limit < 0 or limit > 100:
            raise ValueError('Limit must be between 1 and 100')
        return limit


@app.get("/{bday_id}")
async def get_bday(bday_id: str):
    bday: Birthday = await db.get_bday_by_id(bday_id)
    return BirthdayType.from_object(bday)


@app.get("/list")
async def list_bdays(pagination: PaginationSchema):
    return [BirthdayType.from_object(bday) async for bday in db.list_bdays(**(pagination.dict()))]


@app.get("/search")
async def search_bdays(term: str, pagination: PaginationSchema):
    return [
        BirthdayType.from_object(bday) async for bday in await db.search_bdays_by_name(term, **(pagination.dict()))
    ]

@app.put("/")
async def put_bday(bday: BirthdayType):
    await db.put_bday(bday)
    return bday
