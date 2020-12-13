import sys
from pathlib import Path
import os
import json
import numpy as np
import pickle
from sklearn.cluster import KMeans
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
    data = get_data()
    array = []
    for recipe in data:
        ingredients = json.loads(recipe["ingredients"])
        ingredients_count = len(ingredients)
        description = json.loads(recipe["description"])
        description_length = len(description)
        cooking_time = recipe["cooking_time"]
        rating = recipe["rating"]
        array.append([ingredients_count, description_length, cooking_time, rating])
    numpy_array = np.array(array)
    normalized_array = MinMaxScaler((0,10)).fit_transform(numpy_array)
    return normalized_array


def perform_clustering():
    X = create_numpy_array()
    clustering = KMeans(n_clusters=3, init="k-means++", algorithm="full", n_init=25, random_state=10)
    clustering.fit(X)
    with open(os.path.join(str(path), "app_3ingredients/pickle_objects/clustering_model.pkl"), "wb") as fp:
        pickle.dump(clustering, fp, protocol=4)
    clustering.predict(X)
    relabel = np.choose(clustering.labels_, [1, 2, 3]).astype(np.int64)
    return relabel


def update_categories():
    data = get_data()
    categories = perform_clustering()
    for recipe_number in range(len(data)):
        recipe = Recipe.objects.get(pk=data[recipe_number]["id"])
        recipe.category = categories[recipe_number]
        recipe.save()



