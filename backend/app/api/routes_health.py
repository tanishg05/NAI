import time
import httpx
from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("")
@router.get("/")
@router.get("/health")
async def health_check():
    # Attempt a fast check with Groq to ensure key works
    groq_status = "ok"
    try:
        if settings.GROQ_API_KEY:
            headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
            async with httpx.AsyncClient() as client:
                res = await client.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5.0)
                if res.status_code != 200:
                    groq_status = "invalid_key_or_error"
        else:
            groq_status = "no_key"
    except Exception:
        groq_status = "unreachable"

    return {
        "status": "ok",
        "timestamp": time.time(),
        "groq_api_status": groq_status
    }
