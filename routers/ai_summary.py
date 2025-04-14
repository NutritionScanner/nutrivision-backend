from fastapi import APIRouter
from services.gemini import generate_summary

router = APIRouter(prefix="/ai-summary", tags=["AI Summary"])

@router.get("/{food_item}")
async def get_food_summary(food_item: str):
    """
    Returns an AI-generated nutritional summary along with calories & nutrients.
    """
    summary_data = generate_summary(food_item)
    return {
        "food_item": food_item,
        "summary": summary_data.summary,
        "calories": summary_data.calories,
        "protein": summary_data.protein,
        "carbohydrates": summary_data.carbohydrates,
        "fats": summary_data.fats,
        "fiber": summary_data.fiber,
        "sugar": summary_data.sugar,
        "health_rating": summary_data.health_rating
    }
