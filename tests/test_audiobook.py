# Tests for filetype audiobook

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

SAMPLE = {}


def test_insert_audiobook():
    body = {
        "duration": 10,
        "upload_time": "2022-01-31T12:38:30.167000",
        "title": "a title",
        "author": "auth",
        "narrator": "narrate"
    }
    response = client.post(
        "/api/",
        json={
            "audioFileType": "audiobook",
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


def test_get_audiobook_by_id():
    global SAMPLE
    audiobook = SAMPLE
    response = client.get(f"/api/audiobook/{audiobook['id']}/")
    assert response.status_code == 200
    assert response.json() == audiobook


def test_put_audiobook_by_id():
    global SAMPLE
    audiobook = SAMPLE
    id = audiobook['id']
    del audiobook['id']
    audiobook['title'] = 'another title'
    audiobook['narrator'] = 'another narrator'
    audiobook['author'] = 'another author'
    response = client.put(f"/api/{id}/",
                          json={
                              "audioFileType": "audiobook",
                              "audioFileMetadata": audiobook}
                          )
    audiobook['id'] = id
    assert response.status_code == 200
    assert response.json() == audiobook


def test_delete_audiobook_by_id():
    global SAMPLE
    audiobook = SAMPLE
    response = client.delete(f"/api/audiobook/{audiobook['id']}/")
    assert response.status_code == 200
    response = client.get(f"/api/audiobook/{audiobook['id']}/")
    assert response.status_code == 404
