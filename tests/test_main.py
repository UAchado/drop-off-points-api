from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

urls = {
    "base": "/points/v1",
    "get_all_points": "/points/v1/points",
    "get_point_by_name": "/points/v1/points/name",
    "create_point": "/points/v1/points",
    "get_point_id_of_access": "/points/v1/access",
    "delete_point": "/points/v1/points/name",
}

def test_base():
    response = client.get(urls["base"])
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

@patch("api.main.crud.get_points")
def test_get_all_points(mock_get_points):
    mock_points = [
        {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"},
        {"id": 2, "name": "point2", "location": "location2", "coordinates": "coordinates2", "image": "image2"}
    ]
    mock_get_points.return_value = mock_points
    
    response = client.get(urls["get_all_points"])
    assert response.status_code == 200
    assert response.json() == mock_points

@patch("api.main.crud.get_point_by_name")
def test_get_point_by_name(mock_get_point_by_name):
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_get_point_by_name.return_value = mock_point
    
    response = client.get(urls["get_point_by_name"]+"/point1")
    assert response.status_code == 200
    assert response.json() == mock_point

    mock_get_point_by_name.return_value = None
    response = client.get(urls["get_point_by_name"]+"/999")
    assert response.status_code == 204

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.create_point")
def test_create_point(mock_create_point, mock_get_point_by_name, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_get_point_by_name.return_value = None
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_create_point.return_value = mock_point
    
    response = client.post(urls["create_point"], json = {"name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"})
    assert response.status_code == 201
    assert response.json() == mock_point

    mock_get_point_by_name.return_value = mock_point
    response = client.post(urls["create_point"], json = {"name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"})
    assert response.status_code == 409
    assert response.json() == {"detail": "POINT ALREADY REGISTERED"}

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_auth")
def test_get_point_id_of_access(mock_get_auth, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    
    mock_access = ("fake_name", 1)
    mock_get_auth.return_value = mock_access
    
    response = client.get(urls["get_point_id_of_access"])
    assert response.status_code == 200
    assert response.json() == {
        "name": mock_access[0],
        "point_id": mock_access[1]
    }
    
    mock_get_auth.return_value = (None, None)

    response = client.get(urls["get_point_id_of_access"])
    assert response.status_code == 204

@patch("api.main.auth.verify_access")
@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.delete_point")
def test_delete_point(mock_delete_point, mock_get_point_by_name, mock_verify_access):
    mock_verify_access.return_value = {"user": "dummy_user"}
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "image": "image1"}
    mock_get_point_by_name.return_value = mock_point
    mock_delete_point.return_value = "OK"
    
    response = client.delete(urls["delete_point"]+"/point1")
    assert response.status_code == 200
    assert response.json() == {"message": "POINT DELETED"}

    mock_delete_point.return_value = None
    response = client.delete(urls["delete_point"]+"/999")
    assert response.status_code == 204
