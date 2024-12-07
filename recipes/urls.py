from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('newrecipe/', views.create_recipe, name="new_recipe"),
    path('changerecipe/<str:slug>/', views.edit_recipe, name="change_recipe"),
    path('userpage/<str:username>/', views.user_page, name="userpage"),
    path('recipe/<str:slug>/', views.single_recipe, name="recipe"),
    path('myfollows/', views.follows, name='follows'),
    path('myfavorites/', views.favorites, name='favorites'),
    path('myshoplist/', views.shoplist, name='shoplist'),
    path('download_shopping_list/', views.download_shopping_list, name='download_shopping_list'),
    path('recipe/<str:slug>/delete/', views.delete_recipe, name='delete_recipe'),
    ]
