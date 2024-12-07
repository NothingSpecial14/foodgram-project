# Generated by Django 5.0.7 on 2024-08-06 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_tag_remove_recipe_tag_recipe_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(choices=[('breakfast', 'Завтрак'), ('lunch', 'Обед'), ('dinner', 'Ужин')], max_length=50),
        ),
    ]
