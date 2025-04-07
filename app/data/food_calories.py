"""
Food Calories Database
Contains calorie information for common foods
"""

# Dictionary of common foods and their calorie information
FOOD_CALORIES = {
    # Fruits
    "apple": {
        "calories": 95,
        "portion": "1 medium apple (182g)",
        "details": {
            "food_name": "Apple",
            "nutrients": [
                {"name": "Protein", "value": 0.5, "unit": "g"},
                {"name": "Fat", "value": 0.3, "unit": "g"},
                {"name": "Carbohydrates", "value": 25, "unit": "g"},
                {"name": "Fiber", "value": 4.4, "unit": "g"},
                {"name": "Sugar", "value": 19, "unit": "g"},
                {"name": "Vitamin C", "value": 8.4, "unit": "mg"},
                {"name": "Potassium", "value": 195, "unit": "mg"}
            ]
        }
    },
    "banana": {
        "calories": 105,
        "portion": "1 medium banana (118g)",
        "details": {
            "food_name": "Banana",
            "nutrients": [
                {"name": "Protein", "value": 1.3, "unit": "g"},
                {"name": "Fat", "value": 0.4, "unit": "g"},
                {"name": "Carbohydrates", "value": 27, "unit": "g"},
                {"name": "Fiber", "value": 3.1, "unit": "g"},
                {"name": "Sugar", "value": 14.4, "unit": "g"},
                {"name": "Vitamin C", "value": 10.3, "unit": "mg"},
                {"name": "Potassium", "value": 422, "unit": "mg"}
            ]
        }
    },
    "orange": {
        "calories": 62,
        "portion": "1 medium orange (131g)",
        "details": {
            "food_name": "Orange",
            "nutrients": [
                {"name": "Protein", "value": 1.2, "unit": "g"},
                {"name": "Fat", "value": 0.2, "unit": "g"},
                {"name": "Carbohydrates", "value": 15.4, "unit": "g"},
                {"name": "Fiber", "value": 3.1, "unit": "g"},
                {"name": "Sugar", "value": 12.2, "unit": "g"},
                {"name": "Vitamin C", "value": 69.7, "unit": "mg"},
                {"name": "Potassium", "value": 237, "unit": "mg"}
            ]
        }
    },
    "strawberry": {
        "calories": 46,
        "portion": "1 cup, halves (152g)",
        "details": {
            "food_name": "Strawberries",
            "nutrients": [
                {"name": "Protein", "value": 1, "unit": "g"},
                {"name": "Fat", "value": 0.4, "unit": "g"},
                {"name": "Carbohydrates", "value": 11, "unit": "g"},
                {"name": "Fiber", "value": 3, "unit": "g"},
                {"name": "Sugar", "value": 7, "unit": "g"},
                {"name": "Vitamin C", "value": 84.7, "unit": "mg"},
                {"name": "Potassium", "value": 220, "unit": "mg"}
            ]
        }
    },
    
    # Vegetables
    "carrot": {
        "calories": 50,
        "portion": "1 cup, chopped (128g)",
        "details": {
            "food_name": "Carrot",
            "nutrients": [
                {"name": "Protein", "value": 1.1, "unit": "g"},
                {"name": "Fat", "value": 0.3, "unit": "g"},
                {"name": "Carbohydrates", "value": 12, "unit": "g"},
                {"name": "Fiber", "value": 3.6, "unit": "g"},
                {"name": "Sugar", "value": 6, "unit": "g"},
                {"name": "Vitamin A", "value": 20381, "unit": "IU"},
                {"name": "Potassium", "value": 410, "unit": "mg"}
            ]
        }
    },
    "broccoli": {
        "calories": 55,
        "portion": "1 cup, chopped (91g)",
        "details": {
            "food_name": "Broccoli",
            "nutrients": [
                {"name": "Protein", "value": 3.7, "unit": "g"},
                {"name": "Fat", "value": 0.6, "unit": "g"},
                {"name": "Carbohydrates", "value": 11.2, "unit": "g"},
                {"name": "Fiber", "value": 5.1, "unit": "g"},
                {"name": "Sugar", "value": 2.6, "unit": "g"},
                {"name": "Vitamin C", "value": 135.7, "unit": "mg"},
                {"name": "Potassium", "value": 288, "unit": "mg"}
            ]
        }
    },
    "potato": {
        "calories": 163,
        "portion": "1 medium potato (173g)",
        "details": {
            "food_name": "Potato",
            "nutrients": [
                {"name": "Protein", "value": 4.3, "unit": "g"},
                {"name": "Fat", "value": 0.2, "unit": "g"},
                {"name": "Carbohydrates", "value": 37, "unit": "g"},
                {"name": "Fiber", "value": 3.8, "unit": "g"},
                {"name": "Sugar", "value": 2, "unit": "g"},
                {"name": "Vitamin C", "value": 17.4, "unit": "mg"},
                {"name": "Potassium", "value": 897, "unit": "mg"}
            ]
        }
    },
    "tomato": {
        "calories": 32,
        "portion": "1 medium tomato (123g)",
        "details": {
            "food_name": "Tomato",
            "nutrients": [
                {"name": "Protein", "value": 1.6, "unit": "g"},
                {"name": "Fat", "value": 0.4, "unit": "g"},
                {"name": "Carbohydrates", "value": 7, "unit": "g"},
                {"name": "Fiber", "value": 2.2, "unit": "g"},
                {"name": "Sugar", "value": 4.7, "unit": "g"},
                {"name": "Vitamin C", "value": 23.5, "unit": "mg"},
                {"name": "Potassium", "value": 292, "unit": "mg"}
            ]
        }
    },
    
    # Fast Food & Snacks
    "pizza": {
        "calories": 285,
        "portion": "1 slice of medium pizza (107g)",
        "details": {
            "food_name": "Pizza (Cheese)",
            "nutrients": [
                {"name": "Protein", "value": 12.2, "unit": "g"},
                {"name": "Fat", "value": 10.4, "unit": "g"},
                {"name": "Carbohydrates", "value": 35.7, "unit": "g"},
                {"name": "Fiber", "value": 2.5, "unit": "g"},
                {"name": "Sugar", "value": 3.8, "unit": "g"},
                {"name": "Calcium", "value": 198, "unit": "mg"},
                {"name": "Sodium", "value": 640, "unit": "mg"}
            ]
        }
    },
    "burger": {
        "calories": 354,
        "portion": "1 regular hamburger (110g)",
        "details": {
            "food_name": "Hamburger",
            "nutrients": [
                {"name": "Protein", "value": 15.2, "unit": "g"},
                {"name": "Fat", "value": 15.2, "unit": "g"},
                {"name": "Carbohydrates", "value": 33, "unit": "g"},
                {"name": "Fiber", "value": 1.6, "unit": "g"},
                {"name": "Sugar", "value": 6, "unit": "g"},
                {"name": "Calcium", "value": 126, "unit": "mg"},
                {"name": "Sodium", "value": 497, "unit": "mg"}
            ]
        }
    },
    "french fries": {
        "calories": 312,
        "portion": "1 medium serving (117g)",
        "details": {
            "food_name": "French Fries",
            "nutrients": [
                {"name": "Protein", "value": 3.4, "unit": "g"},
                {"name": "Fat", "value": 15, "unit": "g"},
                {"name": "Carbohydrates", "value": 41, "unit": "g"},
                {"name": "Fiber", "value": 3.8, "unit": "g"},
                {"name": "Sugar", "value": 0.5, "unit": "g"},
                {"name": "Sodium", "value": 210, "unit": "mg"},
                {"name": "Potassium", "value": 643, "unit": "mg"}
            ]
        }
    },
    "chocolate": {
        "calories": 546,
        "portion": "100g chocolate bar",
        "details": {
            "food_name": "Milk Chocolate",
            "nutrients": [
                {"name": "Protein", "value": 7.7, "unit": "g"},
                {"name": "Fat", "value": 33.6, "unit": "g"},
                {"name": "Carbohydrates", "value": 57.9, "unit": "g"},
                {"name": "Fiber", "value": 3.4, "unit": "g"},
                {"name": "Sugar", "value": 51.5, "unit": "g"},
                {"name": "Calcium", "value": 189, "unit": "mg"},
                {"name": "Iron", "value": 0.8, "unit": "mg"}
            ]
        }
    },
    "ice cream": {
        "calories": 273,
        "portion": "1 cup (132g)",
        "details": {
            "food_name": "Vanilla Ice Cream",
            "nutrients": [
                {"name": "Protein", "value": 4.6, "unit": "g"},
                {"name": "Fat", "value": 14.5, "unit": "g"},
                {"name": "Carbohydrates", "value": 31, "unit": "g"},
                {"name": "Sugar", "value": 28, "unit": "g"},
                {"name": "Calcium", "value": 168, "unit": "mg"},
                {"name": "Cholesterol", "value": 58, "unit": "mg"}
            ]
        }
    },
    
    # Beverages
    "coffee": {
        "calories": 2,
        "portion": "1 cup (240ml), black",
        "details": {
            "food_name": "Black Coffee",
            "nutrients": [
                {"name": "Protein", "value": 0.3, "unit": "g"},
                {"name": "Fat", "value": 0, "unit": "g"},
                {"name": "Carbohydrates", "value": 0, "unit": "g"},
                {"name": "Caffeine", "value": 95, "unit": "mg"},
                {"name": "Potassium", "value": 116, "unit": "mg"},
                {"name": "Magnesium", "value": 7.1, "unit": "mg"}
            ]
        }
    },
    "cola": {
        "calories": 139,
        "portion": "1 can (355ml)",
        "details": {
            "food_name": "Cola Soda",
            "nutrients": [
                {"name": "Protein", "value": 0, "unit": "g"},
                {"name": "Fat", "value": 0, "unit": "g"},
                {"name": "Carbohydrates", "value": 39, "unit": "g"},
                {"name": "Sugar", "value": 39, "unit": "g"},
                {"name": "Sodium", "value": 15, "unit": "mg"},
                {"name": "Caffeine", "value": 34, "unit": "mg"}
            ]
        }
    },
    
    # Additional common foods
    "chicken breast": {
        "calories": 165,
        "portion": "100g, cooked",
        "details": {
            "food_name": "Chicken Breast",
            "nutrients": [
                {"name": "Protein", "value": 31, "unit": "g"},
                {"name": "Fat", "value": 3.6, "unit": "g"},
                {"name": "Carbohydrates", "value": 0, "unit": "g"},
                {"name": "Cholesterol", "value": 85, "unit": "mg"},
                {"name": "Sodium", "value": 74, "unit": "mg"},
                {"name": "Potassium", "value": 220, "unit": "mg"}
            ]
        }
    },
    "salmon": {
        "calories": 208,
        "portion": "100g, cooked",
        "details": {
            "food_name": "Salmon",
            "nutrients": [
                {"name": "Protein", "value": 20, "unit": "g"},
                {"name": "Fat", "value": 13, "unit": "g"},
                {"name": "Carbohydrates", "value": 0, "unit": "g"},
                {"name": "Omega-3", "value": 2.3, "unit": "g"},
                {"name": "Vitamin D", "value": 526, "unit": "IU"},
                {"name": "Vitamin B12", "value": 3.2, "unit": "μg"}
            ]
        }
    },
    "rice": {
        "calories": 130,
        "portion": "100g, cooked white rice",
        "details": {
            "food_name": "White Rice",
            "nutrients": [
                {"name": "Protein", "value": 2.7, "unit": "g"},
                {"name": "Fat", "value": 0.3, "unit": "g"},
                {"name": "Carbohydrates", "value": 28, "unit": "g"},
                {"name": "Fiber", "value": 0.4, "unit": "g"},
                {"name": "Iron", "value": 0.2, "unit": "mg"},
                {"name": "Folate", "value": 58, "unit": "μg"}
            ]
        }
    },
    "bread": {
        "calories": 79,
        "portion": "1 slice (30g)",
        "details": {
            "food_name": "White Bread",
            "nutrients": [
                {"name": "Protein", "value": 2.6, "unit": "g"},
                {"name": "Fat", "value": 1, "unit": "g"},
                {"name": "Carbohydrates", "value": 14.3, "unit": "g"},
                {"name": "Fiber", "value": 0.8, "unit": "g"},
                {"name": "Sugar", "value": 1.4, "unit": "g"},
                {"name": "Sodium", "value": 152, "unit": "mg"}
            ]
        }
    },
    "egg": {
        "calories": 77,
        "portion": "1 large egg (50g)",
        "details": {
            "food_name": "Egg",
            "nutrients": [
                {"name": "Protein", "value": 6.3, "unit": "g"},
                {"name": "Fat", "value": 5.3, "unit": "g"},
                {"name": "Carbohydrates", "value": 0.6, "unit": "g"},
                {"name": "Cholesterol", "value": 212, "unit": "mg"},
                {"name": "Vitamin D", "value": 41, "unit": "IU"},
                {"name": "Choline", "value": 147, "unit": "mg"}
            ]
        }
    },
    "pasta": {
        "calories": 158,
        "portion": "100g, cooked",
        "details": {
            "food_name": "Pasta",
            "nutrients": [
                {"name": "Protein", "value": 5.8, "unit": "g"},
                {"name": "Fat", "value": 0.9, "unit": "g"},
                {"name": "Carbohydrates", "value": 31, "unit": "g"},
                {"name": "Fiber", "value": 1.8, "unit": "g"},
                {"name": "Iron", "value": 0.5, "unit": "mg"},
                {"name": "Thiamin", "value": 0.1, "unit": "mg"}
            ]
        }
    },
    "salad": {
        "calories": 152,
        "portion": "1 bowl (100g)",
        "details": {
            "food_name": "Garden Salad with Dressing",
            "nutrients": [
                {"name": "Protein", "value": 2, "unit": "g"},
                {"name": "Fat", "value": 13, "unit": "g"},
                {"name": "Carbohydrates", "value": 7, "unit": "g"},
                {"name": "Fiber", "value": 2.5, "unit": "g"},
                {"name": "Vitamin C", "value": 25, "unit": "mg"},
                {"name": "Vitamin A", "value": 543, "unit": "IU"}
            ]
        }
    }
}

def get_food_calories(food_name):
    """
    Get calorie information for a given food name.
    
    Parameters:
        food_name (str): Name of the food
        
    Returns:
        dict: Calorie information or None if not found
    """
    # Convert to lowercase for case-insensitive matching
    food_name = food_name.lower().strip()
    
    # Exact match
    if food_name in FOOD_CALORIES:
        return FOOD_CALORIES[food_name]
    
    # Check for partial matches
    for key in FOOD_CALORIES:
        if food_name in key or key in food_name:
            return FOOD_CALORIES[key]
    
    # No match found
    return None 