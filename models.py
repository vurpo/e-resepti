"""
This module contains the classes that represent the recipe book and recipe, used in the application.
"""

class RecipeBook:
    """
    Represents a recipe book (collection of recipes)
    """
    def __init__(self, recipes):
        self.recipes = recipes

    @classmethod
    def from_json_list(cls, recipebook):
        """
        Create a RecipeBook from a list deserialized from a JSON array
        """
        recipes = [Recipe.from_json_dict(recipe) for recipe in recipebook]
        return cls(recipes)

    def to_json_list(self):
        """
        Return a list that represents the JSON representation of the recipe book
        """
        return [recipe.to_json_dict() for recipe in self.recipes]

class Recipe:
    """
    Represents a recipe (with name, ingredients, and instructions for how to cook)
    """
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    @classmethod
    def from_json_dict(cls, recipe):
        """
        Create a Recipe from a dict deserialized from a JSON object
        """
        return cls(recipe['name'], recipe['ingredients'], recipe['instructions'])

    def to_json_dict(self):
        """
        Return a dict that represents the JSON representation of the recipe
        """
        return {"name":self.name, "ingredients":self.ingredients, "instructions":self.instructions}
    
    def has_ingredient(self, ingredient_string):
        """
        Check if recipe matches ingredient string
        """
        for ingredient in self.ingredients:
            if ingredient_string.lower() in ingredient['name'].lower():
                return True
        return False

    def prettyprint(self):
        """
        Pretty print recipe for console output
        """
        out = ""
        out += "{}\n".format(self.name)
        out += "{}\n\n".format("="*len(self.name))
        out += "Ingredients:\n"
        for ingredient in self.ingredients:
            out += " * {} {} {}\n".format(ingredient['amount'], ingredient['unit'], ingredient['name'])
        out += "\n"
        out += "{}".format(self.instructions)

        return out
