import models
import sys
import json

"""
This module contains all the command-line interface -specific functions.
All functions take the parameter "recipebook", which is an instance of a RecipeBook to work with.
The command functions return a string, which is what to print out to the command line as a response.
"""

def recipelist(recipebook):
    """
    Returns a list of recipes, for command line output
    """
    out = ""
    out += "Recipes:"
    for index, recipe in enumerate(recipebook.recipes):
        out += "\n{}. {}".format(index, recipe.name)

    return out

def readrecipe(recipebook, index):
    """
    Returns one recipe, for command line output
    """
    try:
        return recipebook.recipes[index].prettyprint()
    except IndexError:
        return "Error: no such recipe"

def newrecipe(recipebook):
    """
    Read a new JSON recipe from command line and add it to recipe book
    """
    new_json = sys.stdin.read()
    try:
        new_dict = json.loads(new_json)
        new_recipe = models.Recipe.from_json_dict(new_dict)
        recipebook.recipes.append(new_recipe)
        return "New recipe added!"
    except json.decoder.JSONDecodeError:
        print("Error: not valid JSON")
        sys.exit(1)
    except KeyError:
        print("Error: not a valid recipe JSON")
        sys.exit(1)

def deleterecipe(recipebook, index):
    """
    Delete one recipe by index from recipe book
    """
    try:
        del recipebook.recipes[index]
    except IndexError:
        print("Error: no such recipe!")
        sys.exit(1)
    return "Recipe deleted."
    

USAGESTRING = """Usage: {} COMMAND
COMMAND can be:
 list - list all recipes
 read <index> - read one recipe
 add - read recipe JSON from stdin and add to recipe book
 delete <index> - delete recipe from recipe book""".format(sys.argv[0])

def main(recipebook, argv):
    """
    Process the command line arguments and pass on to other functions
    """
    if len(argv) >= 2 and argv[1] == "list":
        print(recipelist(recipebook))
    elif len(argv) >= 3 and argv[1] == "read":
        try: print(readrecipe(recipebook, int(argv[2])))
        except ValueError:
            print("Error: index must be integer")
            sys.exit(1)
    elif len(argv) >= 2 and argv[1] == "add":
        print(newrecipe(recipebook))
    elif len(argv) >= 2 and argv[1] == "delete":
        try: print(deleterecipe(recipebook, int(argv[2])))
        except ValueError:
            print("Error: index must be integer")
            sys.exit(1)
    else:
        print(USAGESTRING)
