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


def test_openapi_contains_database_crud_routes() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/auth/register" in paths
    assert "/auth/login" in paths
    assert "/me/" in paths
    assert "/me/profile" in paths
    assert "/me/orders" in paths
    assert "/users/" in paths
    assert "/profiles/" in paths
    assert "/categories/" in paths
    assert "/products/" in paths
    assert "/orders/" in paths


def test_user_validation() -> None:
    response = client.post(
        "/users/",
        json={"name": "A", "email": "not-email", "age": 0},
    )

    assert response.status_code == 422
