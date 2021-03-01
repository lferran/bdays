from fastapi import FastAPI
from pydantic import BaseModel
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
    def from_object(cls, obj: Birthday) -> BirthdayType:
        return cls(
            id=obj.id,
            name=obj.name,
            day=obj.day,
            month=obj.month,
            year=obj.year
        )


class ListBDaysSchema(BaseModel):
    size: Optional[int] = 10
    offset: Optional[int] = None


@app.get("/{bday_id}")
async def get_bday(bday_id: str):
    bday: Birthday = await db.get_bday_by_id(bday_id)
    return BirthdayType.from_object(bday)


@app.get("/list")
async def list_bdays(schema: ListBDaysSchema):
    return [BirthdayType.from_object(bday) async for bday in db.list_bdays(size=schema.size, offset=schema.offset)]


@app.get("/search")
async def search_bdays(name: str):
    return [
        BirthdayType.from_object(bday) async for bday in await db.search_bdays_by_name(name)
    ]

@app.put("/")
async def put_bday(bday: BirthdayType):
    await db.put_bday(bday)
    return bday
