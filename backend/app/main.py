import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import app.api.routes_diet_plan as routes_diet_plan
import app.api.routes_recommendations as routes_recommendations
import app.api.routes_health as routes_health

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables are created on startup
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created.")
    except Exception as e:
        logger.warning(f"Could not connect to database on startup: {e}")
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(routes_diet_plan.router, prefix=f"{settings.API_V1_STR}/diet-plan", tags=["diet-plan"])
app.include_router(routes_recommendations.router, prefix=f"{settings.API_V1_STR}/recommendations", tags=["recommendations"])
