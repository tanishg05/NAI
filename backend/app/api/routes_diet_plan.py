from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import GenerateDietPlanRequest
from app.database import get_db
from app.core.orchestrator import orchestrator
from app.services.nutrition_service import nutrition_service
from app.models.models import User, MealPlan
from app.core.groq_client import AgentGenerationError

router = APIRouter()

@router.post("/generate")
async def generate_diet_plan(request: GenerateDietPlanRequest, db: Session = Depends(get_db)):
    # Prepare payload for agent
    payload = {
        "profile": request.profile.model_dump(),
        "goals": request.goals.model_dump(),
        "preferences": request.preferences.model_dump(),
        "plan_length_days": request.plan_length_days,
        "available_foods": nutrition_service.get_all_foods()
    }
    
    try:
        result = await orchestrator.route("diet_planner", payload)
        
        # Save to DB - mock a user id for now since auth is not required for demo
        user = db.query(User).first()
        if not user:
            user = User(
                name="Demo User",
                age=request.profile.age,
                gender=request.profile.gender,
                height_cm=request.profile.height_cm,
                weight_kg=request.profile.weight_kg,
                activity_level=request.profile.activity_level,
                medical_conditions=request.profile.medical_conditions,
                goal_type=request.goals.goal_type,
                target_calories=request.goals.target_calories,
                diet_type=request.preferences.diet_type,
                cuisine_preference=request.preferences.cuisine_preference,
                allergies=request.preferences.allergies,
                dislikes=request.preferences.dislikes
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Upsert Meal Plan for demo user
        meal_plan = db.query(MealPlan).filter(MealPlan.user_id == user.id).first()
        if not meal_plan:
            meal_plan = MealPlan(user_id=user.id, plan_data=result)
            db.add(meal_plan)
        else:
            meal_plan.plan_data = result
        db.commit()
        db.refresh(meal_plan)
        
        return result
    except AgentGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
