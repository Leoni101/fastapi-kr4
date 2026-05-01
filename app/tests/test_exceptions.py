import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_custom_exception_a_trigger():
    """Тест вызова CustomExceptionA (flag=false)"""
    response = client.get("/trigger-a?flag=false")
    assert response.status_code == 400
    data = response.json()
    assert "CustomExceptionA" in data["error_type"] or "CustomExceptionA" in data["detail"]
    assert data["status_code"] == 400

def test_custom_exception_a_success():
    """Тест успешного запроса (flag=true)"""
    response = client.get("/trigger-a?flag=true")
    assert response.status_code == 200
    assert response.json()["message"] == "Success"
    assert response.json()["flag"] == True

def test_custom_exception_b_trigger():
    """Тест вызова CustomExceptionB (item_id != 42)"""
    response = client.get("/trigger-b/1")
    assert response.status_code == 404
    data = response.json()
    assert "CustomExceptionB" in data["error_type"] or "CustomExceptionB" in data["detail"]
    assert data["status_code"] == 404

def test_custom_exception_b_success():
    """Тест успешного запроса (item_id=42)"""
    response = client.get("/trigger-b/42")
    assert response.status_code == 200
    assert response.json()["message"] == "Success"
    assert response.json()["item_id"] == 42

def test_validation_error():
    """Тест ошибки валидации (Задание 10.2)"""
    # Отправляем некорректные данные (возраст 17, невалидный email, короткий пароль)
    response = client.post(
        "/validate-user",
        json={
            "username": "test_user",
            "age": 17,  # должно быть >18
            "email": "invalid_email",  # невалидный email
            "password": "short",  # слишком короткий
            "phone": "123"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "Validation error" in data["detail"] or "errors" in data

def test_validation_success():
    """Тест успешной валидации"""
    response = client.post(
        "/validate-user",
        json={
            "username": "valid_user",
            "age": 25,
            "email": "valid@example.com",
            "password": "securepass123",
            "phone": "+1234567890"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User data is valid"
    assert data["user"]["username"] == "valid_user"
    assert data["user"]["email"] == "valid@example.com"

def test_validation_missing_phone():
    """Тест валидации без поля phone (должно использовать значение по умолчанию)"""
    response = client.post(
        "/validate-user",
        json={
            "username": "user_no_phone",
            "age": 30,
            "email": "nophone@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["phone"] == "Unknown"