from typing import Optional
from fastapi import Header, HTTPException

# Пример зависимости для аутентификации (можно расширить)
async def common_parameters(
    skip: int = 0,
    limit: int = 10,
    q: Optional[str] = None
):
    return {"skip": skip, "limit": limit, "q": q}

async def verify_api_key(api_key: str = Header(None)):
    if api_key is None:
        raise HTTPException(status_code=400, detail="API Key missing")
    # Здесь можно добавить проверку ключа
    return api_key