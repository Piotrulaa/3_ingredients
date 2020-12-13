from django.urls import path

from . import views

app_name = "app_3ingredients"

urlpatterns = [
    path("", views.EnterIngredientsView.as_view(), name='index'),
    path("results", views.ResultsView.as_view(), name="results"),
    path("results/rate/", views.recipe_rating, name="rate")
]
