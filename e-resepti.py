from flask import Flask, Response, abort, request
import models
import cmdline
import json
import os,sys

"""
This application is a recipe management application with a command-line interface,
and a REST interface. Both interfaces are documented in the file README.md.
"""

app = Flask(__name__)

# Open the recipes.json file and create a RecipeBook object from the JSON in the file
try:
    with open("recipes.json") as recipes_file:
        recipebook = models.RecipeBook.from_json_list(json.load(recipes_file))
except FileNotFoundError: # recipes.json does not exist
    print("Error: no file named \"recipes.json\" found")
    sys.exit(1)

def write_out():
    """
    Write the RecipeBook out to the recipes.json file (and create a backup)
    """
    os.replace("recipes.json", ".recipes.json.backup")
    with open("recipes.json", "w") as recipes_file:
        json.dump(recipebook.to_json_list(),recipes_file)

# REST API endpoints

@app.route("/recipes", methods=['GET', 'POST'])
def recipes():
    """
    Return all recipes (GET) or add new recipe (POST)
    """
    if request.method == 'GET':
        return Response(
                json.dumps(recipebook.to_json_list()),
                mimetype="application/json")
    elif request.method == 'POST':
        new_dict = request.get_json()
        recipebook.recipes.append(models.Recipe.from_json_dict(new_dict))
        write_out()
        return Response(status=200)


@app.route("/recipes/<int:index>", methods=['GET','DELETE'])
def recipe(index):
    """
    Return (GET) or delete (DELETE) one recipe
    """
    try:
        if request.method == 'GET':
            return Response(
                    json.dumps(recipebook.recipes[index].to_json_dict()),
                    mimetype="application/json")
        elif request.method == 'DELETE':
            del recipebook.recipes[index]
            write_out()
            return Response(status=200)
    except IndexError: # recipe with specified index does not exist
        return Response(
                "{\"error\":\"no such recipe\"}",
                status=404,
                mimetype="application/json")

@app.route("/recipes/filter", methods=['GET'])
def filter():
    """
    Filter the array of recipes by a kind of ingredient
    """
    ingredient = request.args.get("ingredient")
    if ingredient == None: # no ingredient parameter was included in the request
        return Response(
            "{\"error\":\"ingredient parameter is required\"}",
            status=400,
            mimetype="application/json")

    recipes = [
            recipe.to_json_dict()
            for recipe in recipebook.recipes
            if recipe.has_ingredient(ingredient)]

    return Response(
            json.dumps(recipes),
            mimetype="application/json")

if __name__ == "__main__": # file was executed as a command line script
    cmdline.main(recipebook, sys.argv)
    write_out()
