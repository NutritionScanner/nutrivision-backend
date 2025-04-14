from fastapi import APIRouter
from services.openfoodfacts import get_nutrition_info
from services.gemini import generate_summary

router = APIRouter(prefix="/nutrition", tags=["Nutrition Data"])

@router.get("/{food_item_or_barcode}")
def fetch_nutrition(food_item_or_barcode: str):
    """
    Determines whether input is a barcode (packaged food) or food name (fresh food).
    """
    if food_item_or_barcode.isnumeric() and len(food_item_or_barcode) > 6:
        # If it's a barcode, fetch packaged food data
        return get_nutrition_info(food_item_or_barcode)
    else:
        # If it's a food name, fetch AI-based summary
        return generate_summary(food_item_or_barcode)
