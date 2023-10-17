from pydantic import BaseModel

class DropoffPoint(BaseModel):
    name: str
    location: str
    coordinates: str
    image: str = None