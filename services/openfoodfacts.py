import requests

OPENFOODFACTS_API = "https://world.openfoodfacts.org/api/v2/product/"

def get_nutrition_info(barcode):
    """Fetches nutrition data from OpenFoodFacts using barcode."""
    response = requests.get(f"{OPENFOODFACTS_API}{barcode}.json")

    if response.status_code != 200:
        return {"error": "Product not found"}

    data = response.json()
    
    if "product" in data:
        product = data["product"]
        return {
            "name": product.get("product_name", "Unknown"),
            "calories": product.get("nutriments", {}).get("energy-kcal_100g", "N/A"),
            "protein": product.get("nutriments", {}).get("proteins_100g", "N/A"),
            "fats": product.get("nutriments", {}).get("fat_100g", "N/A"),
            "carbs": product.get("nutriments", {}).get("carbohydrates_100g", "N/A"),
            "nutriscore": product.get("nutriscore_grade", "N/A"),  # Add Nutri-Score
            "ingredients": product.get("ingredients_text", "N/A"),
        }
    
    return {"error": "Incomplete data"}
