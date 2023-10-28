from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(30), unique = True, index = True)
    location = Column(String(50))
    coordinates = Column(String(200), unique = True)
    photo = Column(String(500))