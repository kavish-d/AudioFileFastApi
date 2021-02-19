# Tests for filetype Podcast

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

SAMPLE = {}


def test_insert_podcast():
    body = {
        "duration": 10,
        "upload_time": "2022-01-31T12:38:30.167000",
        "name": "namae",
        "host": "hoost",
        "participants": ["a", "b"]
    }
    response = client.post(
        "/api/",
        json={
            "audioFileType": "podcast",
            "audioFileMetadata": body}
    )
    assert response.status_code == 200
    res = response.json()
    print(res)
    assert "id" in res
    body['id'] = res['id']
    assert res == body
    global SAMPLE
    SAMPLE = res


def test_get_podcast_by_id():
    global SAMPLE
    podcast = SAMPLE
    response = client.get(f"/api/podcast/{podcast['id']}/")
    assert response.status_code == 200
    assert response.json() == podcast


def test_put_podcast_by_id():
    global SAMPLE
    podcast = SAMPLE
    id = podcast['id']
    del podcast['id']
    podcast['name'] = 'another name'
    podcast['participants'] = ['c', 'd']
    response = client.put(f"/api/{id}/",
                          json={
                              "audioFileType": "podcast",
                              "audioFileMetadata": podcast}
                          )
    podcast['id'] = id
    assert response.status_code == 200
    assert response.json() == podcast


def test_delete_podcast_by_id():
    global SAMPLE
    podcast = SAMPLE
    response = client.delete(f"/api/podcast/{podcast['id']}/")
    assert response.status_code == 200
    response = client.get(f"/api/podcast/{podcast['id']}/")
    assert response.status_code == 404
