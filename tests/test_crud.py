from typing import List
from pytest import fixture
from unittest.mock import patch
from sqlalchemy.orm import Session
from api.db_info import schemas, database, crud, models

## HELPER COMPONENTS

points_bucket = [
    models.Point(name = "Reitoria", location = "Departamento 25", coordinates = "40.631417730224, -8.657526476133642", image = "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_3090.jpg&width=1200"),
    models.Point(name = "CP", location = "Departamento 23", coordinates = "40.62957166653202, -8.655231694880136", image = "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fapi-assets.ua.pt%2Ffiles%2Fimgs%2F000%2F001%2F838%2Foriginal.jpg&width=1200"),
    models.Point(name = "DETI", location = "Departamento 4", coordinates = "40.63331148617483, -8.659589862642955", image = "https://api-assets.ua.pt/files/imgs/000/000/380/original.jpg"),
    models.Point(name = "Cantina de Santiago", location = "Departamento 6", coordinates = "40.630659968175124, -8.659097986459223", image = "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_12306.jpg&width=1200"),
    models.Point(name = "Cantina do Crasto", location = "Departamento M", coordinates = "40.62450887522072, -8.656864475040406", image = "https://api-assets.ua.pt/v1/image/resizer?imageUrl=https%3A%2F%2Fuaonline.ua.pt%2Fupload%2Fimg%2Fjoua_i_2828.JPG&width=1200"),
    models.Point(name = "Pavilhão Aristides Hall", location = "Departamento E", coordinates = "40.63000326980208, -8.654180591479575", image = "https://d1bvpoagx8hqbg.cloudfront.net/originals/bem-vindos-a-ua-399bd8560914b519d0dca3fc57bd0afe.jpg")
]

def add_points_to_db(db: Session, points: List[models.Point]):
    for point in points:
        new_point = models.Point(name = point.name,
                                location = point.location,
                                coordinates = point.coordinates,
                                image = point.image,
                                )
        db.add(new_point)
    db.commit()
    
# BEFORE and AFTER

@fixture(scope="function")
def db():
    connection = database.engine.connect()
    transaction = connection.begin()
    session = database.SessionLocal(bind = connection)

    database.Base.metadata.create_all(bind = connection)

    try:
        yield session
    finally:
        transaction.rollback()
        connection.close()

## UNIT TESTS

def test_get_points(db):
    
    points = crud.get_points(db = db)
    assert len(points) == 0
    assert points == []
    
    add_points_to_db(db = db, points = points_bucket)
    
    points = crud.get_points(db = db)
    assert len(points) == 6
    assert points[0].name == points_bucket[0].name
    
def test_get_point_id(db):
    
    point = crud.get_point_id(db = db, id = 1)
    assert point == None

    add_points_to_db(db, points_bucket)
    
    all_points = crud.get_points(db = db)
    assert len(all_points) != 0

    point = crud.get_point_id(db = db, id = all_points[0].id)
    assert point != None
    assert point.id == all_points[0].id

def test_get_point_by_name(db):
    
    point = crud.get_point_by_name(db = db, name = "Reitoria")
    assert point == None

    add_points_to_db(db, points_bucket)

    point = crud.get_point_by_name(db = db, name = "Reitoria")
    assert point != None
    assert point.name == points_bucket[0].name

@patch("api.db_info.auth.verify_access")
def test_get_auth(mock_verify_access, db):
    mock_verify_access.return_value = {"sub":"None"}
    
    access = crud.get_auth(db = db, request = None)
    assert access == (None, None)

    add_points_to_db(db, [points_bucket[0]])
    point = crud.get_points(db)[0]
    new_entry = models.AuthorizationToPoint(
                                sub = "fake_sub_identifier",
                                name = "fake_name",
                                point_id = point.id,
                                )
    db.add(new_entry)
    db.commit()
    
    mock_verify_access.return_value = {"sub":"fake_sub_identifier"}
    
    access = crud.get_auth(db = db, request = None)
    assert access == ("fake_name", point.id)

def test_create_point(db):
    
    new_point = schemas.PointCreate(
        name = "new_name",
        location = "new_location",
        coordinates = "new_coordinates",
        image = "new_image"
    )
    
    point = crud.create_point(db = db, new_point = new_point)
    assert point != None
    assert point.name == new_point.name
    
    points = crud.get_points(db = db)
    assert len(points) == 1

def test_delete_point(db):
    
    points = crud.get_points(db = db)
    assert len(points) == 0
    
    return_value = crud.delete_point(db = db, name = "Reitoria")
    assert return_value == None
    
    add_points_to_db(db, [points_bucket[0]])
    
    points = crud.get_points(db = db)
    assert len(points) == 1
    
    points_in_db = points[0]
    return_value = crud.delete_point(db = db, name = points_in_db.name)
    assert return_value == "OK"
    
    points = crud.get_points(db = db)
    assert len(points) == 0