from fastapi import HTTPException, Request
from jose import jwt, JWTError
from typing import Dict, Any

from ..core.config import settings

def decode_token(request: Request, token_name: str) -> Dict[str, Any]:
    try:
        request_token = request.cookies.get(token_name)
        if not request_token:
            raise HTTPException(status_code=401, detail="Token not found")
        return jwt.decode(request_token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
