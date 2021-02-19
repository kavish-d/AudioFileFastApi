# Tests for filetype song

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

SAMPLE = {}


def test_insert_song_past_time():
    response = client.post(
        "/api/",
        json={
            "audioFileType": "song",
            "audioFileMetadata": {
                "duration": 10,
                "upload_time": "2020-01-31T12:38:30.167000",
                "name": "namae"
            }
        }

    )
    assert response.status_code == 422


def test_insert_song_zero_duration():
    response = client.post(
        "/api/",
        json={
            "audioFileType": "song",
            "audioFileMetadata": {
                "duration": 0,
                "upload_time": "2022-01-31T12:38:30.167000",
                "name": "namae"
            }
        }

    )
    assert response.status_code == 422


def test_insert_song():
    body = {
        "duration": 10,
        "upload_time": "2022-01-31T12:38:30.167000",
        "name": "namae",
    }
    response = client.post(
        "/api/",
        json={
            "audioFileType": "song",
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


def test_get_song_by_id():
    global SAMPLE
    song = SAMPLE
    response = client.get(f"/api/song/{song['id']}/")
    assert response.status_code == 200
    assert response.json() == song


def test_put_song_by_id_wrong_time():
    global SAMPLE
    song = SAMPLE.copy()
    id = song['id']
    del song['id']
    song['name'] = 'another name'
    song['upload_time'] = "2018-01-31T12:38:30.167000"
    response = client.put(f"/api/{id}/",
                          json={
                              "audioFileType": "song",
                              "audioFileMetadata": song}
                          )
    assert response.status_code == 422


def test_put_song_by_id():
    global SAMPLE
    song = SAMPLE
    id = song['id']
    del song['id']
    song['name'] = 'another name'
    response = client.put(f"/api/{id}/",
                          json={
                              "audioFileType": "song",
                              "audioFileMetadata": song}
                          )
    song['id'] = id
    assert response.status_code == 200
    assert response.json() == song


def test_delete_song_by_id():
    global SAMPLE
    song = SAMPLE
    response = client.delete(f"/api/song/{song['id']}/")
    assert response.status_code == 200
    response = client.get(f"/api/song/{song['id']}/")
    assert response.status_code == 404
