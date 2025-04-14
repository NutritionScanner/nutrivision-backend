from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import  JWTError, jwt
from datetime import datetime, timedelta
import os

from models.user import UserCreate, UserResponse
from services.connect_database import get_db
from sqlalchemy import text

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# Helper: Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

# Register User
@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    try:
        db.execute(
            text("""
                INSERT INTO users (username, password, gender, age, height_cm, current_weight, goal_weight, goal_type, weight_change_speed)
                VALUES (:username, :password, :gender, :age, :height_cm, :current_weight, :goal_weight, :goal_type, :weight_change_speed)
            """),
            {
                "username": user.username,
                "password": hashed_password,
                "gender": user.gender,
                "age": user.age,
                "height_cm": user.height_cm,
                "current_weight": user.current_weight,
                "goal_weight": user.goal_weight,
                "goal_type": user.goal_type,
                "weight_change_speed": user.weight_change_speed,
            },
        )
        db.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# User Login
@router.post("/login", response_model=dict)
def login(user: UserCreate, db: Session = Depends(get_db)):
    user_record = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": user.username}).fetchone()
    if not user_record or not pwd_context.verify(user.password, user_record.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get User Info (Protected)
@router.get("/user", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**dict(user._mapping))
