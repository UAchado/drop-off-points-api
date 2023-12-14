from typing import Optional
from pydantic import BaseModel

class PointBase(BaseModel):
    name: str
    location: str
    coordinates: str
    image: Optional[str]

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
                "image": "link_to_image"
            }
        }

class AuthorizationToPoint(BaseModel):
    id: int
    sub: str
    point_id: int

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "id" : 1,
                "sub": "sub_identifier",
                "point_id": 1,
            }
        }