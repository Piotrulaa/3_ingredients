from django import forms


class EnterIngredientsForm(forms.Form):
    ingredient_1 = forms.CharField(required=False)
    ingredient_2 = forms.CharField(required=False)
    ingredient_3 = forms.CharField(required=False)
