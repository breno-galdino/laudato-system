from fastapi import HTTPException
from jose import jwt, JWTError
from typing import Dict, Any

from ..core.config import settings

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
