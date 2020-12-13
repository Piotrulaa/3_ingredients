import os
import sys
from django.core.management.base import BaseCommand, CommandError

path = os.path.dirname((os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if path not in sys.path:
    sys.path.append(path)
from app_3ingredients.update_categories import update_categories
from app_3ingredients.categorize import categorize_new_recipes


class Command(BaseCommand):
    help = "Updates categories of the recipes:"

    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", help="Update algorithm which assigns categories to recipes and assign new categories to all of them")
        parser.add_argument("--new", action="store_true", help="Use current algorithm to assign categories to new recipes")

    def handle(self, *args, **options):
        if options["all"]:
            update_categories()
            self.stdout.write(self.style.SUCCESS("Algorithm and categories updated succesfully!"))
        elif options["new"]:
            categorize_new_recipes()
            self.stdout.write(self.style.SUCCESS("Categories assigned succesfully!"))
        else:
            raise CommandError("Argument required. Type <command> --help for possible arguments.")


