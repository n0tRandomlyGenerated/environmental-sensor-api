from fastapi import APIRouter
import secrets
from app import config

auth_router = APIRouter()

@auth_router.post("/generate-api-key")
def generate_api_key():
    config.CURRENT_API_KEY = secrets.token_hex(16)
    return {"api_key": config.CURRENT_API_KEY}