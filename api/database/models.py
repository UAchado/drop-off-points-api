from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, unique=True)
    coordinates = Column(String, unique=True)
    photo = Column(String, unique=True)
    personnel = Column(list[Integer])
    items = Column(list[Integer])
