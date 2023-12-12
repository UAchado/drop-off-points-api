from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

def test_base():
    response = client.get("/points/v1/")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_points")
def test_get_all_points(mock_get_points, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_points = [
        {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"},
        {"id": 2, "name": "point2", "location": "location2", "coordinates": "coordinates2", "image": "image2"}
    ]
    mock_get_points.return_value = mock_points
    
    response = client.get("/points/v1/points/")
    assert response.status_code == 200
    assert response.json() == mock_points

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_point_by_name")
def test_get_point_by_name(mock_get_point_by_name, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_get_point_by_name.return_value = mock_point
    
    response = client.get("/points/v1/points/name/point1")
    assert response.status_code == 200
    assert response.json() == mock_point

    mock_get_point_by_name.return_value = None
    response = client.get("/points/v1/points/name/999")
    assert response.status_code == 204

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.create_point")
def test_create_point(mock_create_point, mock_get_point_by_name, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_get_point_by_name.return_value = None
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_create_point.return_value = mock_point
    
    response = client.post("/points/v1/points/", json = {"name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"})
    assert response.status_code == 201
    assert response.json() == mock_point

    mock_get_point_by_name.return_value = mock_point
    response = client.post("/points/v1/points/", json = {"name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"})
    assert response.status_code == 409
    assert response.json() == {"detail": "POINT ALREADY REGISTERED"}

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_auth_by_email")
def test_get_point_id_of_access(mock_get_auth_by_email, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    
    email = "FakeEmail"
    mock_access = 1
    mock_get_auth_by_email.return_value = mock_access
    
    response = client.get(f"/points/v1/access/{email}")
    assert response.status_code == 200
    assert response.json() == mock_access
    
    mock_get_auth_by_email.return_value = None

    response = client.get(f"/points/v1/access/{email}")
    assert response.status_code == 204

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.delete_point")
def test_delete_point(mock_delete_point, mock_get_point_by_name, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_get_point_by_name.return_value = mock_point
    mock_delete_point.return_value = "OK"
    
    response = client.delete("/points/v1/points/name/point1")
    assert response.status_code == 200
    assert response.json() == {"message": "POINT DELETED"}

    mock_delete_point.return_value = None
    response = client.delete("/points/v1/points/name/point999")
    assert response.status_code == 204
