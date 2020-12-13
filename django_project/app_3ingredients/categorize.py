import sys
from pathlib import Path
import os
import pickle
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler

path = Path(__file__).resolve().parent.parent
if path not in sys.path:
    sys.path.append(str(path))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from app_3ingredients.models import Recipe


def get_data():
    queryset = Recipe.objects.all()
    data = list(queryset.values())
    return data


def create_numpy_array():
    uncategorized = Recipe.objects.filter(category=0)
    if uncategorized:
        data = get_data()
        array = []
        uncategorized_array = []
        for recipe in data:
            ingredients = json.loads(recipe["ingredients"])
            ingredients_count = len(ingredients)
            description = json.loads(recipe["description"])
            description_length = len(description)
            cooking_time = recipe["cooking_time"]
            rating = recipe["rating"]
            category = recipe["category"]
            array.append([ingredients_count, description_length, cooking_time, rating, category])
        numpy_array = np.array(array)
        normalized_array = MinMaxScaler((0,10)).fit_transform(numpy_array)
        for row in normalized_array:
            if int(row[4]) == 0:
                uncategorized_array.append([row[0], row[1], row[2], row[3]])
        normalized_uncategorized_array = np.array(uncategorized_array)
        return normalized_uncategorized_array


def categorize():
    X = create_numpy_array()
    if X is not None:
        with open(os.path.join(str(path), "app_3ingredients/pickle_objects/clustering_model.pkl"), "rb") as fp:
            clustering_model = pickle.load(fp)
        relabel = np.choose(clustering_model.predict(X), [1, 2, 3]).astype(np.int64)
        return relabel


def categorize_new_recipes():
    categories = categorize()
    if categories is not None:
        queryset = Recipe.objects.filter(category=0)
        data = list(queryset.values())
        for recipe_number in range(len(data)):
            recipe = Recipe.objects.get(pk=data[recipe_number]["id"])
            recipe.category = categories[recipe_number]
            recipe.save()

