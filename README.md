# 3_ingredients
This app was a part of my engineering thesis on Wrocław University
of Science and Technology. It allows user to find recipes for dishes
containing specified ingredients.

### How it works
User can enter up to 3 ingredients in search form, and receive in
response a list of recipes from app database, in which they are used.
Beside these ingredients, recipes can contain any number of other
ingredients. User can also rate the recipe if he likes it.

### Usage of Machine Learning
App uses clustering algorithm *k-means++* for dividing recipes into three
groups, based on parameters like number of ingredients, cooking time,
number of steps in recipe and how they were rated by users. These 
groups are used to provide variety in search results.

### Search results
Search algorithm tries to provide different types of recipes on each
results page. When possible, each page will contain at least one of 
top rated recipes, and one recipe from each group created by clustering
algorithm.
