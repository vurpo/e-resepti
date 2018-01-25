# E-Resepti

E-resepti is a CLI and REST application for managing recipes.

To begin, create the virtualenv and enter it:

```
$ virtualenv env -p $(which python3)
$ source env/bin/activate
```

Then, install the dependencies:

```
(env) $ pip install -r requirements.txt`
```

## Command-line interface

The file `e-resepti.py` can be executed, with a command (and parameters) as its parameters. The script reads the recipes from a `recipes.json` file in its working directory. Before modifying the `recipes.json` file, the script creates a backup file containing the current contents at `.recipes.json.backup`. The command can be:

### `list`

Lists the names of all the recipes in the book.

### `read <index>`

Prints out a recipe, formatted for reading.

### `add`

Read a recipe in JSON format (see below) and add it to the recipe book.

Hint: if you want to type the JSON at the terminal, you can do the following:

```
$ python e-resepti.py add <<EOF
> /* type recipe JSON here */
> EOF
New recipe added!
$
```

### `delete <index>`

Deletes a recipe from the recipe book.

## REST API

The file `e-resepti.py` is also a Flask app that serves a REST API for managing the recipe book.

```
(env) $ FLASK_APP=e-resepti.py flask run
```

The endpoints served are:

### GET /recipes

`[Recipe]`

Returns a list of all recipes in JSON format (see below).

### GET /recipes/{index}

`Recipe`

Returns one recipe (indexed by the order returned in GET /recipes)

### GET /recipes/filter?ingredient={ingredient}

`[Recipe]`

Returns all recipes where some ingredient matches the supplied search term.

### POST /recipes

Adds a new recipe to the recipe book (body in JSON format).

### DELETE /recipes/{index}

Deletes recipe from recipe book

## JSON data models

### `Recipe`

`name` (`String`): Name of the recipe

`ingredients` (`[Ingredient]`): Ingredients required for the recipe

`instructions` (`String`): Instructions for how to complete the recipe

### `Ingredient`

`amount` (`Number`): amount of ingredient

`unit` (`String`): unit of the amount

`name` (`String`): name of the ingredient
