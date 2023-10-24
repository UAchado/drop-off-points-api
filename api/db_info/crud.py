from sqlalchemy.orm import Session

from . import models, schemas

def get_point(db: Session, point_id: int):
    return db.query(models.Point).filter(models.Point.id == point_id).first()

def get_points(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Point).offset(skip).limit(limit).all()

def get_point_by_name(db:Session, name: str):
    return db.query(models.Point).filter(models.Point.name == name).first()

def create_point(db:Session, new_point: schemas.PointCreate):
    db_point = models.Point(name=new_point.name, location=new_point.location, coordinates=new_point.coordinates, photo=new_point.photo)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def delete_point(db:Session, point: schemas.Point):
    point = db.query(models.Point).filter(models.Point.id == point.id).first()
    db.delete(point)
    db.commit()
    db.refresh()
    if get_point_by_name(point.name):
        return "ERROR"
    return "OK"
