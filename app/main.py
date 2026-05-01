from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routers import products, users
from app.exceptions import CustomExceptionA, CustomExceptionB, custom_exception_a_handler, custom_exception_b_handler, ErrorResponse
from app.schemas import User

# Создаём приложение FastAPI
app = FastAPI(
    title="Контрольная работа №4",
    description="API для демонстрации миграций, исключений, валидации и тестов",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(products.router)
app.include_router(users.router)

# Регистрируем обработчики пользовательских исключений (Задание 10.1)
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)

# Кастомный обработчик ошибок валидации (Задание 10.2)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": 422,
            "detail": "Validation error",
            "errors": exc.errors(),
            "error_type": "ValidationError"
        }
    )

# Эндпоинты для демонстрации пользовательских исключений (Задание 10.1)
@app.get("/trigger-a")
async def trigger_exception_a(flag: bool = False):
    """Эндпоинт, который вызывает CustomExceptionA при flag=false"""
    if not flag:
        raise CustomExceptionA("Flag is false - raising CustomExceptionA")
    return {"message": "Success", "flag": flag}

@app.get("/trigger-b/{item_id}")
async def trigger_exception_b(item_id: int):
    """Эндпоинт, который вызывает CustomExceptionB при item_id != 42"""
    if item_id != 42:
        raise CustomExceptionB(f"Item {item_id} not found - raising CustomExceptionB")
    return {"message": "Success", "item_id": item_id}

# Эндпоинт для валидации пользователя (Задание 10.2)
@app.post("/validate-user", status_code=status.HTTP_200_OK)
async def validate_user(user: User):
    """Валидация данных пользователя с помощью Pydantic"""
    return {
        "message": "User data is valid",
        "user": user.model_dump()
    }

# Корневой эндпоинт
@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в API контрольной работы №4",
        "endpoints": {
            "products": "/products",
            "users": "/users",
            "validation": "/validate-user (POST)",
            "exceptions": "/trigger-a?flag=false, /trigger-b/{item_id}"
        },
        "docs": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}