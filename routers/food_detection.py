import shutil
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.food_recognition import detect_food
from services.fruit_vegetable_detector import detect_fruit_or_vegetable
from services.gemini import generate_summary

router = APIRouter(prefix="/food-detection", tags=["Food Detection"])

# Ensure the static directory exists
os.makedirs("static", exist_ok=True)

@router.post("/food-item")
async def classify_food(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = f"static/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detect food item
        food_label = detect_food(file_path)

        # Get nutrition summary from Gemini
        nutrition_info = generate_summary(food_label)

        # Clean up the uploaded file after processing
        os.remove(file_path)

        # Return the nutrition information as a dictionary
        return nutrition_info if isinstance(nutrition_info, dict) else nutrition_info.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/fruit-vegetable")
async def classify_fruit_or_vegetable(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = f"static/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detect fruit or vegetable
        fruit_label = detect_fruit_or_vegetable(file_path)

        # Get nutrition summary from Gemini
        nutrition_info = generate_summary(fruit_label)

        # Clean up the uploaded file after processing
        os.remove(file_path)

        # Return the nutrition information as a dictionary
        return nutrition_info if isinstance(nutrition_info, dict) else nutrition_info.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
