from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI template is running"}


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_users_crud_flow() -> None:
    create_response = client.post(
        "/users/",
        json={"name": "Charlie Brown", "email": "charlie@example.com", "age": 28},
    )

    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]
    assert created_user["name"] == "Charlie Brown"

    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 200
    assert get_response.json()["email"] == "charlie@example.com"

    update_response = client.put(
        f"/users/{user_id}",
        json={"name": "Charlie Updated", "email": "updated@example.com", "age": 29},
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Charlie Updated"

    delete_response = client.delete(f"/users/{user_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404


def test_user_validation() -> None:
    response = client.post(
        "/users/",
        json={"name": "A", "email": "not-email", "age": 0},
    )

    assert response.status_code == 422
