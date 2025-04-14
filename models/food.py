from pydantic import BaseModel

class FoodDetectionResponse(BaseModel):
    food_item: str

class NutritionResponse(BaseModel):
    name: str
    calories: str
    proteins: str
    fats: str
    carbs: str

class NutritionSummary:
    def __init__(self, summary, calories, protein, carbohydrates, fats, fiber, sugar, health_rating):
        self.summary = summary
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.fiber = fiber
        self.sugar = sugar
        self.health_rating = health_rating

    def to_dict(self):
        return {
            "summary": self.summary,
            "calories": self.calories,
            "protein": self.protein,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
            "fiber": self.fiber,
            "sugar": self.sugar,
            "health_rating": self.health_rating
        }
