from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import database

class Point(database.Base):
    """
    Represents a point in a database.

    :param id: The unique identifier of the point.
    :type id: int
    :param name: The name of the point.
    :type name: str
    :param location: The location description of the point.
    :type location: str
    :param coordinates: The coordinates of the point.
    :type coordinates: str
    :param image: The image URL of the point.
    :type image: str
    """
    __tablename__ = "points"

    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    name = Column(String(30), unique = True, index = True)
    location = Column(String(50))
    coordinates = Column(String(200), unique = True)
    image = Column(String(500))
    
class AuthorizationToPoint(database.Base):
    """
    This class is responsible for authorizing access to a specific point.

    :class:`AuthorizationToPoint` inherits from the base class :class:`database.Base` and is mapped to the database table "authpoint".

    Attributes:
        id (int): The primary key for the authorization record.
        sub (str): The subject (user) being authorized.
        name (str): The subject name
        point_id (int): The foreign key to the associated point.
        dropoff_point (:class:`Point`): The reference to the associated point.

    """
    __tablename__ = "authpoint"
    
    id = Column(Integer, primary_key = True, index = True, autoincrement=True)
    sub = Column(String(50), unique = True)
    name = Column(String(50))
    point_id = Column(Integer, ForeignKey('points.id'))
    
    dropoff_point = relationship("Point")