# Read Test
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

file_type = ['song', 'audiobook', 'podcast']


def test_read():
    for f in file_type:
        response = client.get(f"/api/{f}/")
        assert response.status_code == 200
    # Test Wrong file type value
    response = client.get(f"/api/asdasd/")
    assert response.status_code == 422
