from django.views.generic import FormView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.core import serializers
from django.http import JsonResponse
import json

from .forms import EnterIngredientsForm
from .models import Recipe


class EnterIngredientsView(FormView):
    form_class = EnterIngredientsForm
    template_name = "form_view.html"
    success_url = "results"

    def post(self, request, *args, **kwargs):
        request.session["ingredients"] = [
            request.POST["ingredient_1"],
            request.POST["ingredient_2"],
            request.POST["ingredient_3"]
        ]
        request.session["results"] = None
        return super(EnterIngredientsView, self).post(request, *args, **kwargs)


class ResultsView(ListView):
    template_name = "list_view.html"
    context_object_name = "recipes"
    request = None
    extra_context = None
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.extra_context = {"ingredients": request.session.get("ingredients")}
        self.request = request
        return super(ResultsView, self).get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if not self.request.session.get("results"):
            queryset = self.search_recipes()
            serialized_queryset = json.loads(serializers.serialize("json", queryset))
            json_context = (self.create_json_context(serialized_queryset))
            self.request.session["results"] = json_context
            return json_context
        else:
            for result in self.request.session.get("results"):
                recipe = Recipe.objects.get(pk=result["id"])
                result["rating"] = recipe.rating
            return self.request.session.get("results")

    def search_recipes(self):
        top_rated = self.filter_by_ingredients().order_by("-rating")
        category_1 = self.filter_by_ingredients().filter(category=1).order_by("?")
        category_2 = self.filter_by_ingredients().filter(category=2).order_by("?")
        category_3 = self.filter_by_ingredients().filter(category=3).order_by("?")

        results = []
        current_ids = []
        top_rated_count = len(top_rated)
        category_1_count = len(category_1)
        category_2_count = len(category_2)
        category_3_count = len(category_3)

        for iteration in range(top_rated_count):
            if top_rated[iteration].pk not in current_ids:
                current_ids.append(top_rated[iteration].pk)
                results.append(top_rated[iteration])
            if iteration < category_1_count:
                if category_1[iteration].pk not in current_ids:
                    current_ids.append(category_1[iteration].pk)
                    results.append(category_1[iteration])
            if iteration < category_2_count:
                if category_2[iteration].pk not in current_ids:
                    current_ids.append(category_2[iteration].pk)
                    results.append(category_2[iteration])
            if iteration < category_3_count:
                if category_3[iteration].pk not in current_ids:
                    current_ids.append(category_3[iteration].pk)
                    results.append(category_3[iteration])
        return results

    def filter_by_ingredients(self):
        return Recipe.objects.filter(
            ingredients__icontains=self.extra_context["ingredients"][0]
        ).filter(
            ingredients__icontains=self.extra_context["ingredients"][1]
        ).filter(
            ingredients__icontains=self.extra_context["ingredients"][2]
        )

    def create_json_context(self, serialized_queryset):
        json_context = []
        for recipe in serialized_queryset:
            ingredients = json.loads(recipe["fields"]["ingredients"])
            description = json.loads(recipe["fields"]["description"])
            cooking_time = f'{int(recipe["fields"]["cooking_time"]/60)}:{(recipe["fields"]["cooking_time"]%60):02d} h'
            json_context.append({
                "id": recipe["pk"],
                "title": recipe["fields"]["title"],
                "ingredients": ingredients,
                "description": description,
                "cooking_time": cooking_time,
                "servings": recipe["fields"]["servings"],
                "url": recipe["fields"]["url"],
                "rating": recipe["fields"]["rating"]
            })
        return json_context


def recipe_rating(request):
    if request.method == "POST":
        recipe_id = request.POST.get("recipe_id")
        value = request.POST.get("value")
        recipe_obj = Recipe.objects.get(id=recipe_id)
        rating = recipe_obj.rating
        if value == "Unlike" and rating > 0:
            rating -= 1
        elif value == "Looks delicious!":
            rating += 1
        recipe_obj.rating = rating
        recipe_obj.save()
        data = {
            "value": value,
            "rating": rating
        }
        response = JsonResponse(data, safe=False)
        if value == "Looks delicious!":
            response.set_cookie(f"rated_{recipe_id}", value, max_age=60*60*24*365*2, samesite="Lax")
        return response
    return redirect("app_3ingredients:results")
