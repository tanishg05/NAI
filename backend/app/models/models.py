from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # Profile
    age = Column(Integer)
    gender = Column(String)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(String)
    medical_conditions = Column(JSON, default=list)
    
    # Goals
    goal_type = Column(String)
    target_calories = Column(Integer, nullable=True)
    
    # Preferences
    diet_type = Column(String)
    cuisine_preference = Column(String)
    allergies = Column(JSON, default=list)
    dislikes = Column(JSON, default=list)

    meal_plans = relationship("MealPlan", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_data = Column(JSON) # Stores the JSON schema matched payload
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="meal_plans")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendation_data = Column(JSON) # Stores list of recommendations
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
