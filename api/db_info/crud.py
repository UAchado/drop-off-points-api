import json
import os
from fastapi import Request
from sqlalchemy.orm import Session

from . import models, schemas, auth

def get_points(db: Session):
    """
    :param db: The database session object to use for querying.
    :return: A list of all points in the database.
    """
    return db.query(models.Point).all()

def get_point_id(db: Session, id: int):
    """
    :param db: A database session object of type Session.
    :param id: An integer representing the id of the point.
    :return: The Point object corresponding to the given id, or None if no such point exists.

    """
    return db.query(models.Point).filter(models.Point.id == id).first()

def get_point_by_name(db: Session, name: str):
    """
    Retrieve a point from the database based on its name.

    :param db: The database session.
    :param name: The name of the point.
    :return: The point with the given name, or None if not found.
    """
    return db.query(models.Point).filter(models.Point.name == name).first()

def get_auth(db: Session, request: Request):
    """
    :param db: The database session.
    :param request: The request object containing the user access token.
    :return: The point ID associated with the user's authorization, or None if the user has no access.

    """
    decoded_token = auth.verify_access(request)
    sub = decoded_token["sub"]
    access = db.query(models.AuthorizationToPoint).filter(models.AuthorizationToPoint.sub == sub).first()
    if access != None:
        return (access.name, access.point_id)
    return (None, None)

def create_point(db: Session, new_point: schemas.PointCreate):
    """
    Create Point

    Inserts a new point into the database.

    :param db: The database session.
    :param new_point: The data for the new point.
    :return: The newly created point.
    """
    db_point = models.Point(name = new_point.name,
                            location = new_point.location, 
                            coordinates = new_point.coordinates, 
                            image = new_point.image)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def delete_point(db: Session, name: str):
    """
    Delete a point from the database.

    :param db: The session to the database.
    :type db: Session
    :param name: The name of the point to delete.
    :type name: str
    :return: A string indicating the result of the deletion, either "OK" if successful or None if the point was not found.
    :rtype: str or None
    """
    db_point = get_point_by_name(db, name)
    if db_point == None:
        return None
    db.delete(db_point)
    db.commit()
    return "OK"
