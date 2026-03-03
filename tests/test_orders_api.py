import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.api.dependencies import get_db
from app.infrastructure.database.base import Base
from main_api import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "nombre": "Test User",
            "email": "test@example.com",
            "password": "123456",
        },
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "123456",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "nombre": "Juan",
            "email": "juan@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "juan@example.com"


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "nombre": "Juan",
            "email": "juan@example.com",
            "password": "123456",
        },
    )
    response = client.post(
        "/auth/login",
        data={
            "username": "juan@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_crear_orden(client, auth_headers):
    response = client.post(
        "/orders/",
        json={
            "cliente": "Test User",
            "items": [
                {"nombre": "Laptop", "precio": 15000, "cantidad": 1},
                {"nombre": "Mouse", "precio": 300, "cantidad": 2},
            ],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["total"] == 15600


def test_listar_ordenes(client, auth_headers):
    client.post(
        "/orders/",
        json={
            "cliente": "Test User",
            "items": [{"nombre": "Laptop", "precio": 15000, "cantidad": 1}],
        },
        headers=auth_headers,
    )
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_eliminar_orden(client, auth_headers):
    order = client.post(
        "/orders/",
        json={
            "cliente": "Test User",
            "items": [{"nombre": "Laptop", "precio": 15000, "cantidad": 1}],
        },
        headers=auth_headers,
    ).json()
    response = client.delete(f"/orders/{order['id']}", headers=auth_headers)
    assert response.status_code == 204


def test_orden_no_encontrada(client, auth_headers):
    response = client.get("/orders/999", headers=auth_headers)
    assert response.status_code == 404
