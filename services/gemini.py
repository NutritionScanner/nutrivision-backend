from google import genai
from pydantic import BaseModel
import os

# Define the response schema using Pydantic
class NutritionSummary(BaseModel):
    food_item: str
    summary: str
    calories: str
    protein: str
    carbohydrates: str
    fats: str
    fiber: str
    sugar: str
    health_rating: str
    average_serving_size: str
    calories_per_serving: str
    serving_notes: str


# Initialize the Gemini client with API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(food_item: str) -> NutritionSummary:
    """
    Generates a structured nutritional summary and key nutrients of the specified food item
    using the Gemini 2.0 Flash model.
    """
    prompt = f"""
    Provide a structured nutritional breakdown for {food_item} in JSON format.
    Include the following data fields:
    {{
        "food_item": "{food_item}",
        "summary": "Brief nutritional and health benefits summary",
        "calories": "Calories per 100g",
        "protein": "Protein content in grams per 100g",
        "carbohydrates": "Carbs content in grams per 100g",
        "fats": "Fat content in grams per 100g",
        "fiber": "Fiber content in grams per 100g",
        "sugar": "Sugar content in grams per 100g",
        "health_rating": "Healthy / Moderate / Unhealthy",
        "average_serving_size": "Description or weight (g) of a typical serving",
        "calories_per_serving": "Estimated calories per typical serving",
        "serving_notes": "Additional remarks on the serving size"
    }}
    Return the pure JSON without extra commentary.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": NutritionSummary,
        },
    )

    # Return parsed response if available
    if response.parsed:
        structured_data = response.parsed
    else:
        structured_data = NutritionSummary(
            food_item=food_item,
            summary="N/A",
            calories="N/A",
            protein="N/A",
            carbohydrates="N/A",
            fats="N/A",
            fiber="N/A",
            sugar="N/A",
            health_rating="Unknown",
            average_serving_size="N/A",
            calories_per_serving="N/A",
            serving_notes="N/A"
        )

    return structured_data
 