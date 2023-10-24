import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from api.main import app, get_db

class TestFastAPI(unittest.TestCase):
    def test_base(self):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"response": "Hello World!"}

    def test_base2(self):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 201
        assert response.json() == {"response": "Hello World!"}

    # @patch('main.database.SessionLocal')
    # def test_get_all_points(self, mock_db):
    #     mock_session = Mock()
    #     mock_db.return_value = mock_session
    #     mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []

    #     client = TestClient(app)
    #     response = client.get("/points/")
    #     assert response.status_code == 200
    #     assert response.json() == []

    # @patch('main.database.SessionLocal')
    # def test_create_point(self, mock_db):
    #     mock_session = Mock()
    #     mock_db.return_value = mock_session
    #     mock_session.query.return_value.filter.return_value.first.return_value = None
    #     mock_session.add.return_value = None
    #     mock_session.commit.return_value = None
    #     mock_session.refresh.return_value = None

    #     client = TestClient(app)
    #     response = client.post("/points/", json={"name": "point1"})
    #     assert response.status_code == 200
    #     assert response.json() == {"id": 1, "name": "point1"}

    # @patch('main.database.SessionLocal')
    # def test_delete_point(self, mock_db):
    #     mock_session = Mock()
    #     mock_db.return_value = mock_session
    #     mock_session.query.return_value.filter.return_value.first.return_value = {"id": 1, "name": "point1"}
    #     mock_session.delete.return_value = None
    #     mock_session.commit.return_value = None

    #     client = TestClient(app)
    #     response = client.delete("/point/point1")
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "Point deleted"}

    #     mock_session.delete.return_value = "Error"
    #     response = client.delete("/point/point1")
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "Error"}

if __name__ == '__main__':
    unittest.main()
