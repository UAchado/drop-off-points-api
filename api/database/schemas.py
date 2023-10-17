from pydantic import BaseModel

class PointBase(BaseModel):
    name: str
    location: str
    coordinates: str
    photo: str

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int
    personnel: list[int] = []
    items: list[int] = []

    class Config:
        orm_mode = True