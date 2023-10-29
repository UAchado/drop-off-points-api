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
        from_attributes = True
        schema_extra = {
            "example": {
                "id" : 1,
                "name": "Room 123",
                "location": "Department of Eletronics",
                "coordinates": "-123456789 123456",
                "photo": "link_to_photo"
            }
        }