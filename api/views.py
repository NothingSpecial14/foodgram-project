from users.models import Subscription
from recipes.models import Ingredient, Recipe, Favorite, Purchase
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
import json
User=get_user_model()



# @login_required
# def is_subscribed(request, author_id):
#     subscriber = request.user
#     subscribed_to = get_object_or_404(User, pk=author_id)
#     is_subscribed = Subscription.objects.filter(subscriber=subscriber, subscribed_to=subscribed_to).exists()
#     return JsonResponse({'is_subscribed': is_subscribed})
                                        

@login_required
def subscribe(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается POST.')
    try:
        data = json.loads(request.body.decode('utf-8'))
        id=data.get('id')
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Некорректный ID пользователя.'}, status=400)
    subscriber=request.user
    subscribed_to=get_object_or_404(User, id=id)
    if subscriber == subscribed_to:
        return JsonResponse({'error': 'Нельзя подписаться на самого себя.'}, status=400)
    existing_subscription = Subscription.objects.filter(
        subscriber=subscriber,
        subscribed_to=subscribed_to
    ).exists()
    if existing_subscription:
        return JsonResponse({'error': 'Вы уже подписаны на этого пользователя.'}, status=400)       
    
    subscription=Subscription.objects.create(subscriber=subscriber, subscribed_to=subscribed_to)
    return JsonResponse({
        'message': 'Вы успешно подписались на пользователя.',
        'subscription_id': subscription.id
    }, status=201)


@login_required
def unsubscribe(request, id):
    if request.method != 'DELETE':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается DELETE.')
    subscriber = request.user
    subscribed_to = get_object_or_404(User, id=id)
    try:
        subscription = Subscription.objects.get(subscriber=subscriber, subscribed_to=subscribed_to)
        subscription.delete()
        return JsonResponse({'message': 'Вы успешно отписались от пользователя.'}, status=200)
    except Subscription.DoesNotExist:
        return JsonResponse({'error': 'Вы не подписаны на этого пользователя.'}, status=400)
    

@login_required
def get_ingredient(request):
    text = request.GET.get('query')
    ingredients_list = Ingredient.objects.filter(name__istartswith=text)
    listy = []
    for ingredient in ingredients_list:
        dicty = {}
        dicty['title'] = ingredient.name
        dicty['dimension'] = ingredient.unit
        listy.append(dicty)

    print(listy)
    return JsonResponse(listy, safe=False)


@login_required
def create_favorite(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается POST.')
    try:
        data = json.loads(request.body.decode('utf-8'))
        id=data.get('id')
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Некорректный ID рецепта.'}, status=400)
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    existing_favorite = Favorite.objects.filter(user=user, recipe=recipe).exists()
    if existing_favorite:
        return JsonResponse({'error': 'Вы уже добавили этот рецепт в избранное.'}, status=400)
    favorite = Favorite.objects.create(user=user, recipe=recipe)
    return JsonResponse({
        'message': 'Рецепт успешно добавлен в избранное.',
        'favorite_id': favorite.id
    }, status=201)


@login_required
def delete_favorite(request, id):
    if request.method != 'DELETE':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается DELETE.')
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    try:
        favorite = Favorite.objects.get(user=user, recipe=recipe)
        favorite.delete()
        return JsonResponse({'message': 'Рецепт успешно удалён из избранного.'}, status=200)
    except Favorite.DoesNotExist:
        return JsonResponse({'error': 'Вы не добавляли этот рецепт в избранное.'}, status=400)
    


@login_required
def add_purchase(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается POST.')
    try:
        data = json.loads(request.body.decode('utf-8'))
        id=data.get('id')
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Некорректный ID рецепта.'}, status=400)
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    existing_favorite = Purchase.objects.filter(user=user, recipe=recipe).exists()
    if existing_favorite:
        return JsonResponse({'error': 'Вы уже добавили этот рецепт в покупки.'}, status=400)
    purchase = Purchase.objects.create(user=user, recipe=recipe)
    return JsonResponse({
        'message': 'Рецепт успешно добавлен в покупки-.',
        'purchase_id': purchase.id
    }, status=201)



@login_required
def delete_purchase(request, id):
    if request.method != 'DELETE':
        return HttpResponseBadRequest('Некорректный метод HTTP. Ожидается DELETE.')
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    try:
        purchase = Purchase.objects.get(user=user, recipe=recipe)
        purchase.delete()
        return JsonResponse({'message': 'Рецепт успешно удалён из списка покупок.'}, status=200)
    except Favorite.DoesNotExist:
        return JsonResponse({'error': 'Вы не добавляли этот рецепт в покупки.'}, status=400)
    