from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
from itertools import count
from threading import Lock
from typing import Dict, Any

router = APIRouter(prefix="/users", tags=["users"])

# In-memory хранилище (Задание 11.1 и 11.2)
db: Dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)

class UserIn(BaseModel):
    username: str
    age: int

class UserOut(BaseModel):
    id: int
    username: str
    age: int

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    """Создание нового пользователя"""
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """Получение пользователя по ID"""
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Удаление пользователя"""
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)

# Дополнительный эндпоинт для получения всех пользователей (для удобства тестирования)
@router.get("/", response_model=list[UserOut])
def get_all_users():
    """Получение всех пользователей"""
    return [{"id": user_id, **user_data} for user_id, user_data in db.items()]