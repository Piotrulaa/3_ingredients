# Generated by Django 3.1.3 on 2020-11-19 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('cooking_time', models.IntegerField()),
                ('servings', models.IntegerField()),
                ('url', models.TextField()),
                ('rating', models.IntegerField()),
                ('group', models.IntegerField()),
            ],
        ),
    ]
