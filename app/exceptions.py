from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Пользовательские исключения (Задание 10.1)
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "CustomExceptionA: Invalid request"):
        super().__init__(status_code=400, detail=detail)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "CustomExceptionB: Resource not found"):
        super().__init__(status_code=404, detail=detail)

# Модель для ответа с ошибкой
class ErrorResponse(BaseModel):
    status_code: int
    detail: str
    error_type: str

# Обработчики исключений
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            detail=exc.detail,
            error_type="CustomExceptionA"
        ).dict()
    )

async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            detail=exc.detail,
            error_type="CustomExceptionB"
        ).dict()
    )