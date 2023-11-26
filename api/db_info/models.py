from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import database

class Point(database.Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String(30), unique = True, index = True)
    location = Column(String(50))
    coordinates = Column(String(200), unique = True)
    photo = Column(String(500))