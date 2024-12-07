from typing import Any
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Recipe, Tag, Ingredient, RecipeIngredient, Favorite, Purchase
from django.db import models
from users.models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Tag) 
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display=('name', 'unit')
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('amount', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display=('author', 'name', 'show_liked')
    search_fields=('name', 'igredients')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug':('name',)}
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple(attrs={'class': 'checkbox-inline'})},
    }
    inlines = [RecipeIngredientInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['tags'].widget.attrs.update({'class':'checkbox-inline'})
        return form
    
    def show_liked(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    show_liked.short_description = "Favorite count"

 

# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_filter = ('email', 'username')
  
@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    pass

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass