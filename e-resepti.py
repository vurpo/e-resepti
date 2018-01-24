from flask import Flask, Response, abort, request
import models
import cmdline
import json
import os,sys

app = Flask(__name__)

try:
    with open("recipes.json") as recipes_file:
        recipebook = models.RecipeBook.from_json_list(json.load(recipes_file))
except FileNotFoundError:
    print("Error: no file named \"recipes.json\" found")
    sys.exit(1)

"""Write the JSON data out to the recipes.json file (and create a backup)"""
def write_out():
    os.replace("recipes.json", ".recipes.json.backup")
    with open("recipes.json", "w") as recipes_file:
        json.dump(recipebook.to_json_list(),recipes_file)

# REST API endpoints

"""Return all recipes or add new recipe"""
@app.route("/recipes", methods=['GET', 'POST'])
def recipes():
    if request.method == 'GET':
        return Response(
                json.dumps(recipebook.to_json_list()),
                mimetype="application/json")
    elif request.method == 'POST':
        new_dict = request.get_json()
        recipebook.recipes.append(models.Recipe.from_json_dict(new_dict))
        write_out()
        return Response(status=200)


"""Return or delete one recipe"""
@app.route("/recipes/<int:index>", methods=['GET','DELETE'])
def recipe(index):
    try:
        if request.method == 'GET':
            return Response(
                    json.dumps(recipebook.recipes[index].to_json_dict()),
                    mimetype="application/json")
        elif request.method == 'DELETE':
            del recipebook.recipes[index]
            write_out()
            return Response(status=200)
    except IndexError:
        return Response(
                "{\"error\":\"no such recipe\"}",
                status=404,
                mimetype="application/json")

"""Filter the array of recipes by a kind of ingredient"""
@app.route("/recipes/filter", methods=['GET'])
def filter():
    ingredient = request.args.get("ingredient")
    if ingredient == None:
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

if __name__ == "__main__":
    cmdline.main(recipebook, sys.argv)
    write_out()
