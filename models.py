"""Represents a recipe book (collection of recipes)"""
class RecipeBook:
    def __init__(self, recipes):
        self.recipes = recipes

    """Create a RecipeBook from a list deserialized from a JSON array"""
    @classmethod
    def from_json_list(cls, recipebook):
        recipes = []
        for recipe in recipebook:
            recipes.append(Recipe.from_json_dict(recipe))
        return cls(recipes)

    """Return a list that represents the JSON representation of the recipe book"""
    def to_json_list(self):
        return [recipe.to_json_dict() for recipe in self.recipes]

"""Represents a recipe (with name, ingredients, and instructions for how to cook)"""
class Recipe:
    """Standard constructor"""
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    """Create a Recipe from a dict deserialized from a JSON object"""
    @classmethod
    def from_json_dict(cls, recipe):
        return cls(recipe['name'], recipe['ingredients'], recipe['instructions'])

    """Return a dict that represents the JSON representation of the recipe"""
    def to_json_dict(self):
        return {"name":self.name, "ingredients":self.ingredients, "instructions":self.instructions}
    
    """Check if recipe matches ingredient string"""
    def has_ingredient(self, ingredient_string):
        for ingredient in self.ingredients:
            if ingredient_string.lower() in ingredient['name'].lower():
                return True
        return False

    """Pretty print recipe for console output"""
    def prettyprint(self):
        out = ""
        out += "{}\n".format(self.name)
        out += "{}\n\n".format("="*len(self.name))
        out += "Ingredients:\n"
        for ingredient in self.ingredients:
            out += " * {} {} {}\n".format(ingredient['amount'], ingredient['unit'], ingredient['name'])
        out += "\n"
        out += "{}".format(self.instructions)

        return out
