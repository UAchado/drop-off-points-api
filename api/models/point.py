from pydantic import BaseModel

class Point(BaseModel):
    name: str
    location: str
    coordinates: str
    image: str = None