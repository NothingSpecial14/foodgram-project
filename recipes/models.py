from typing import Iterable
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from unidecode import unidecode



User = get_user_model()

def transliterate_and_slugify(value):
    if not value:
        return ''
    return slugify(unidecode(value))
    

class Ingredient(models.Model):

    name=models.CharField(max_length=100)
    unit=models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})"
    
    
class Tag(models.Model):

    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    TAG_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LUNCH, 'Обед'),
        (DINNER, 'Ужин')
    ]
    name = models.CharField(max_length=50, choices=TAG_CHOICES)

    def __str__(self) -> str:
        return dict(self.TAG_CHOICES).get(self.name)
    
    
    
class Recipe(models.Model):

    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', )
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='recipes', blank=True)
    description=models.TextField(max_length=5000)
    ingredients=models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags=models.ManyToManyField(Tag, related_name='recipes')
    cooking_time=models.PositiveIntegerField()
    slug=models.SlugField(unique=True, blank=True)
    pub_date=models.DateTimeField('Дата публикации рецепта', auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug=transliterate_and_slugify(self.name)+('-by-')+slugify(self.author.username)
        super().save(*args, **kwargs)

    def is_purchased_by(self, user):
        return Purchase.objects.filter(recipe=self, user=user).exists()

    def is_favorited_by(self, user):
        return Favorite.objects.filter(recipe=self, user=user).exists()



class RecipeIngredient(models.Model):
    recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient=models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount=models.PositiveIntegerField()


class Favorite(models.Model):
    recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likers')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} добавил в избранное {self.recipe}"

    class Meta:
        unique_together = ('user', 'recipe')


class Purchase(models.Model):
    recipe=models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='buyers')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} добавил в покупки {self.recipe}"

    class Meta:
        unique_together = ('user', 'recipe')
