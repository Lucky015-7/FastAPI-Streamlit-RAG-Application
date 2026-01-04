from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    # Tests if the server is alive
    response = client.get("/list-docs")
    assert response.status_code == 200
