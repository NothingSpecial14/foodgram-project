from django.urls import path
from .views import *

urlpatterns = [
    path('subscriptions/', subscribe, name='add_subscription'),
    path('subscriptions/<int:id>/', unsubscribe, name='remove_subscription'),
    path('ingredients/', get_ingredient, name='get_ingredient'),
    path('favorites/', create_favorite, name='add_favorite'),
    path('favorites/<int:id>/', delete_favorite, name='remove_favorite'),
    path('purchases/',add_purchase, name='add_purchase'),
    path('purchases/<int:id>/',delete_purchase, name='remove_purchase')
]
