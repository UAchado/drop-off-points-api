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

    class ConfigDict:
        from_attributes  = True