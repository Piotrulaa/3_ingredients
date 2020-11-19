from django.db import models


class Recipes(models.Model):
    title = models.TextField()
    ingredients = models.TextField()
    description = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    url = models.TextField()
    rating = models.IntegerField()
    group = models.IntegerField()

