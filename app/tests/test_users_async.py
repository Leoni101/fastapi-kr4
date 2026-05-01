import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from app.main import app
from app.routers.users import db

fake = Faker()

# Фикстура для очистки in-memory БД перед каждым тестом
@pytest.fixture(autouse=True)
def clear_db():
    """Очищает базу данных перед каждым тестом"""
    db.clear()
    yield

@pytest.mark.asyncio
async def test_create_user():
    """Тест создания пользователя (успешный сценарий)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/", json={"username": "john_doe", "age": 30})
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "john_doe"
        assert data["age"] == 30

@pytest.mark.asyncio
async def test_create_user_with_faker():
    """Тест создания пользователя с генерацией данных через Faker"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        username = fake.user_name()
        age = fake.random_int(min=18, max=100)
        
        response = await ac.post("/users/", json={"username": username, "age": age})
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == username
        assert data["age"] == age

@pytest.mark.asyncio
async def test_get_existing_user():
    """Тест получения существующего пользователя"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Сначала создаём пользователя
        create_resp = await ac.post("/users/", json={"username": "existing_user", "age": 25})
        user_id = create_resp.json()["id"]
        
        # Получаем пользователя
        response = await ac.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "existing_user"
        assert data["age"] == 25

@pytest.mark.asyncio
async def test_get_nonexistent_user():
    """Тест получения несуществующего пользователя (404)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/99999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_existing_user():
    """Тест удаления существующего пользователя (204)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Создаём пользователя
        create_resp = await ac.post("/users/", json={"username": "to_delete", "age": 35})
        user_id = create_resp.json()["id"]
        
        # Удаляем пользователя
        delete_resp = await ac.delete(f"/users/{user_id}")
        
        assert delete_resp.status_code == 204
        
        # Проверяем, что пользователь действительно удалён
        get_resp = await ac.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_user():
    """Тест повторного удаления несуществующего пользователя (404)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Пытаемся удалить несуществующего пользователя
        response = await ac.delete("/users/99999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user_twice():
    """Тест удаления одного пользователя дважды (сначала 204, потом 404)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Создаём пользователя
        create_resp = await ac.post("/users/", json={"username": "double_delete", "age": 28})
        user_id = create_resp.json()["id"]
        
        # Первое удаление
        first_delete = await ac.delete(f"/users/{user_id}")
        assert first_delete.status_code == 204
        
        # Второе удаление (должно вернуть 404)
        second_delete = await ac.delete(f"/users/{user_id}")
        assert second_delete.status_code == 404

@pytest.mark.asyncio
async def test_create_user_boundary_age():
    """Тест создания пользователя с граничными значениями возраста"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Возраст должен быть > 18, но валидация только в Pydantic (для /validate-user)
        # Здесь возраст может быть любым
        response = await ac.post("/users/", json={"username": "young_user", "age": 19})
        
        assert response.status_code == 201
        data = response.json()
        assert data["age"] == 19