from pydantic import BaseModel
from typing import Optional

# Input model for registration and goal update
class UserCreate(BaseModel):
    username: str
    password: str
    gender: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    current_weight: Optional[float] = None
    goal_weight: Optional[float] = None
    goal_type: Optional[str] = None
    weight_change_speed: Optional[float] = None

# Output model for user response
class UserResponse(BaseModel):
    id: int
    username: str
    gender: Optional[str]
    age: Optional[int]
    height_cm: Optional[float]
    current_weight: Optional[float]
    goal_weight: Optional[float]
    goal_type: Optional[str]
    weight_change_speed: Optional[float]
