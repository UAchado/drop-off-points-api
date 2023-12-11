from sqlalchemy.orm import Session

from . import models, schemas

def get_points(db: Session):
    return db.query(models.Point).all()

def get_point_id(db: Session, id: int):
    return db.query(models.Point).filter(models.Point.id == id).first()

def get_point_by_name(db: Session, name: str):
    return db.query(models.Point).filter(models.Point.name == name).first()

def get_auth_by_email(db: Session, email: str):
    access = db.query(models.AuthorizationToPoint).filter(models.AuthorizationToPoint.email == email).first()
    if access != None:
        return access.point_id
    return None

def create_point(db: Session, new_point: schemas.PointCreate):
    db_point = models.Point(name = new_point.name, 
                            location = new_point.location, 
                            coordinates = new_point.coordinates, 
                            image = new_point.image)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def delete_point(db: Session, name: str):
    db_point = get_point_by_name(db, name)
    if db_point == None:
        return None
    db.delete(db_point)
    db.commit()
    return "OK"
