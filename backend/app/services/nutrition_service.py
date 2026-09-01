import json
import os

class NutritionService:
    def __init__(self):
        self.available_foods = self._load_data()

    def _load_data(self):
        filepath = os.path.join(os.path.dirname(__file__), "../data/indian_food_nutrition.json")
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def get_all_foods(self):
        return self.available_foods

nutrition_service = NutritionService()
