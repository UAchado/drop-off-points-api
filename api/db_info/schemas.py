from typing import Optional
from pydantic import BaseModel

class PointBase(BaseModel):
    """
    The `PointBase` class is a subclass of `BaseModel` and represents a point with a name, location, coordinates, and an optional image.

    Attributes:
        - name (str): The name of the point.
        - location (str): The location of the point.
        - coordinates (str): The coordinates of the point.
        - image (Optional[str]): The optional image associated with the point.

    Examples:
        >>> point = PointBase(name="Point A", location="City A", coordinates="1.234,5.678", image="image.jpg")
        >>> point.name
        'Point A'
        >>> point.location
        'City A'
        >>> point.coordinates
        '1.234,5.678'
        >>> point.image
        'image.jpg'
    """
    name: str
    location: str
    coordinates: str
    image: Optional[str]

class PointCreate(PointBase):
    """
    A class representing a point created by the user.

    This class inherits from the PointBase class.

    .. note::
        The PointCreate class is used to represent points that are created by the user.

    .. seealso::
        :py:class:`PointBase`

    """
    pass

class Point(PointBase):
    """
    Represents a point in a 2D coordinate system.

    Attributes:
        id (int): The unique identifier for the point.
    """
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
    """
    AuthorizationToPoint class is used to represent an authorization to access a specific point.

    Attributes:
        - id (int): The unique identifier of the authorization.
        - sub (str): The subject identifier of the authorization.
        - point_id (int): The identifier of the point that the authorization grants access to.

    ConfigDict:
        - from_attributes (bool): If set to True, the class will be configured to load data from attributes.
        - schema_extra (dict): Extra schema information for serialization and documentation purposes.

    Example:
        The example below shows how an AuthorizationToPoint object can be represented:

        {
            "id": 1,
            "sub": "sub_identifier",
            "point_id": 1
        }
    """
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