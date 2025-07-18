from fastapi import HTTPException, Header
from app import config

def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    if x_api_key != config.CURRENT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key