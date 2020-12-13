from django.db import models


class Recipe(models.Model):
    title = models.TextField()
    ingredients = models.TextField()
    description = models.TextField()
    cooking_time = models.IntegerField()
    servings = models.IntegerField()
    url = models.TextField()
    rating = models.IntegerField()
    category = models.IntegerField(null=True)

