import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session

client = TestClient(app)

# Фикстура для очистки БД перед каждым тестом
@pytest.fixture(autouse=True)
def clean_db():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)

def test_create_product():
    """Тест создания продукта"""
    response = client.post(
        "/products/",
        json={"title": "Test Product", "price": 99.99, "count": 5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["price"] == 99.99
    assert data["count"] == 5
    assert "id" in data
    assert "description" in data

def test_get_products_empty():
    """Тест получения списка продуктов (пустой)"""
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_products_with_data():
    """Тест получения списка продуктов (с данными)"""
    # Создаём продукт
    client.post("/products/", json={"title": "Product 1", "price": 10, "count": 1})
    client.post("/products/", json={"title": "Product 2", "price": 20, "count": 2})
    
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_product_by_id():
    """Тест получения продукта по ID"""
    create_resp = client.post("/products/", json={"title": "Test", "price": 50, "count": 3})
    product_id = create_resp.json()["id"]
    
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["title"] == "Test"

def test_get_nonexistent_product():
    """Тест получения несуществующего продукта"""
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_update_product():
    """Тест обновления продукта"""
    create_resp = client.post("/products/", json={"title": "Old", "price": 10, "count": 1})
    product_id = create_resp.json()["id"]
    
    update_resp = client.put(
        f"/products/{product_id}",
        json={"title": "New", "price": 20, "count": 2, "description": "Updated description"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New"
    assert update_resp.json()["description"] == "Updated description"

def test_delete_product():
    """Тест удаления продукта"""
    create_resp = client.post("/products/", json={"title": "To Delete", "price": 100, "count": 1})
    product_id = create_resp.json()["id"]
    
    delete_resp = client.delete(f"/products/{product_id}")
    assert delete_resp.status_code == 204
    
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404