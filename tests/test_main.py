from fastapi.testclient import TestClient
from unittest.mock import patch
from api import main

client = TestClient(main.app)

def test_base():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"response": "Hello World!"}

@patch("api.main.crud.get_points")
def test_get_all_points(mock_get_points):
    mock_points = [
        {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "photo": "photo1"},
        {"id": 2, "name": "point2", "location": "location2", "coordinates": "coordinates2", "photo": "photo2"}
    ]
    mock_get_points.return_value = mock_points
    
    response = client.get("/points/")
    assert response.status_code == 200
    assert response.json() == mock_points

@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.create_point")
def test_create_point(mock_create_point, mock_get_point_by_name):
    mock_get_point_by_name.return_value = None
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "photo": "photo1"}
    mock_create_point.return_value = mock_point
    
    response = client.post("/points/", json={"name": "point1", "location": "location1", "coordinates": "coordinates1", "photo": "photo1"})
    assert response.status_code == 201
    assert response.json() == mock_point

@patch("api.main.crud.get_point_by_name")
@patch("api.main.crud.delete_point")
def test_delete_point(mock_delete_point, mock_get_point_by_name):
    mock_point = {"id": 1, "name": "point1", "location": "location1", "coordinates": "coordinates1", "photo": "photo1"}
    mock_get_point_by_name.return_value = mock_point
    mock_delete_point.return_value = "OK"
    
    response = client.delete("/point/point1")
    assert response.status_code == 200
    assert response.json() == {"message": "Point deleted"}
