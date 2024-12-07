from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from .forms import RecipeForm
from django.core.paginator import Paginator
from users.models import Subscription
from django.http import QueryDict, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.utils.text import slugify
from unidecode import unidecode
from django.db.models import Sum, F

User = get_user_model()

#def transliterate_and_slugify(value):
    #if not value:
        #return ''
    #return slugify(unidecode(value))
    

def index(request):
    tags = request.GET.getlist('tags')
    latest_recipes = Recipe.objects.order_by('-pub_date')
    if tags:
        latest_recipes = latest_recipes.filter(tags__name__in=tags).distinct().order_by('-pub_date')
    paginator = Paginator(latest_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = ['breakfast', 'lunch', 'dinner']
    tags_params = {}
    for tag in all_tags:
        current_tags = tags.copy()
        if tag in current_tags:
            current_tags.remove(tag)
        else:
            current_tags.append(tag)
        params = QueryDict(mutable=True)
        for t in current_tags:
            params.update({'tags': t})
        tags_params[tag] = params.urlencode()
    if request.user.is_authenticated:

        purchase_recipes_ids = []
        purchase_recipes_ids = Purchase.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        favorite_recipes_ids = []
        favorite_recipes_ids = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
    else:
        purchase_recipes_ids = []
        favorite_recipes_ids = []
    context = {
        'page': page,
        'selected_tags': tags,
        'paginator': paginator,
        'tags_params': tags_params,
        'favorite_recipes_ids':favorite_recipes_ids,
        'purchase_recipes_ids':purchase_recipes_ids
    }
    return render(request, 'index.html', context)
                                                                                



def user_page(request, username):
    user=get_object_or_404(User, username__iexact=username)
    user_recipes = Recipe.objects.filter(author=user).order_by("-pub_date")
    tags = request.GET.getlist('tags')
    if tags:
         user_recipes = user_recipes.filter(tags__name__in=tags).distinct().order_by("-pub_date")
    paginator = Paginator(user_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = ['breakfast', 'lunch', 'dinner']
    tags_params = {}
    for tag in all_tags:
        current_tags = tags.copy()
        if tag in current_tags:
            current_tags.remove(tag)
        else:
            current_tags.append(tag)
        params = QueryDict(mutable=True)
        for t in current_tags:
            params.update({'tags': t})
        tags_params[tag] = params.urlencode()
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, subscribed_to=user).exists()
        purchase_recipes_ids = []
        purchase_recipes_ids = Purchase.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        favorite_recipes_ids =[]
        favorite_recipes_ids = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
    else:
        purchase_recipes_ids = []
        favorite_recipes_ids = []
    context = {
        'selected_tags': tags,
         'user':user,
         'page':page,
         'paginator':paginator,
         'tags_params': tags_params,
         'is_subscribed':is_subscribed,
         'favorite_recipes_ids':favorite_recipes_ids,
         'purchase_recipes_ids':purchase_recipes_ids
    }
    return render(request, 'authorRecipe.html', context)


@login_required
def favorites(request):
    fav_recipes = Recipe.objects.filter(likers__user=request.user).order_by("-pub_date")
    tags = request.GET.getlist('tags')
    if tags:
         fav_recipes = fav_recipes.filter(tags__name__in=tags).distinct().order_by("-pub_date")
    paginator = Paginator(fav_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = ['breakfast', 'lunch', 'dinner']
    tags_params = {}
    for tag in all_tags:
        current_tags = tags.copy()
        if tag in current_tags:
            current_tags.remove(tag)
        else:
            current_tags.append(tag)
        params = QueryDict(mutable=True)
        for t in current_tags:
            params.update({'tags': t})
        tags_params[tag] = params.urlencode()
        purchase_recipes_ids = []
        purchase_recipes_ids = Purchase.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        context={
        'selected_tags': tags,
        'page':page,
        'paginator':paginator,
        'tags_params': tags_params,
        'purchase_recipes_ids':purchase_recipes_ids,
        }
    return render(request, 'favorite.html', context)

def get_ingredients_json(recipe):
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    ingredients_data = []
    for ri in recipe_ingredients:
        ingredients_data.append({
            'name': ri.ingredient.name,
            'value': ri.amount,
            'units': ri.ingredient.unit
        })
    return json.dumps(ingredients_data)


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            slug = transliterate_and_slugify(recipe.name) + '-by-' + slugify(recipe.author.username)
            recipe.slug = slug
            if Recipe.objects.filter(slug=recipe.slug).exists():
                form.add_error('name', 'Рецепт с таким названием уже существует. Пожалуйста, выберите другое название.')
                return render(request, 'formRecipe.html', {'form': form})
            recipe.save()
            form.save_m2m()
            ingredients_data = request.POST.get('ingredients_data')
            if not ingredients_data:
                form.add_error(None, 'Добавьте хотя бы один ингредиент.')
                return render(request, 'formRecipe.html', {'form': form})
            else:
                ingredients = json.loads(ingredients_data)
                for ingredient in ingredients:
                    name = ingredient.get('name')
                    amount = ingredient.get('value')
                    units = ingredient.get('units')
                    ingredient_obj, created = Ingredient.objects.get_or_create(
                        name=name,
                        defaults={'unit': units}
                    )
                    
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient_obj, amount=amount)
                
                return redirect('recipe', slug=recipe.slug)
        else:
            print('Form errors:', form.errors)
            return render(request, 'formRecipe.html', {'form':form})
    else:
        form = RecipeForm()
    return render(request,'formRecipe.html', {'form':form})
 

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author.id != request.user.id:
        return redirect('recipe', slug=slug)
    if request.method =='POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            slug = transliterate_and_slugify(recipe.name) + '-by-' + slugify(recipe.author.username)
            recipe.slug = slug
            if Recipe.objects.filter(slug=recipe.slug).exclude(pk=recipe.pk).exists():
                form.add_error('name', 'Рецепт с таким названием уже существует. Пожалуйста, выберите другое название.')
                return render(request, 'formChangeRecipe.html', {'form': form, 'recipe': recipe})

            ingredients_data = request.POST.get('ingredients_data')
            if not ingredients_data:
                form.add_error(None, 'Добавьте хотя бы один ингредиент.')
                return render(request, 'formChangeRecipe.html', {'form': form, 'recipe': recipe})
            else:
                ingredients = json.loads(ingredients_data)
                recipe.save()
                form.save_m2m()
                # Удаляем старые ингредиенты рецепта
                RecipeIngredient.objects.filter(recipe=recipe).delete()
                for ingredient in ingredients:
                    name = ingredient.get('name')
                    amount = ingredient.get('value')
                    units = ingredient.get('units')
                    ingredient_obj, created = Ingredient.objects.get_or_create(
                        name=name,
                        defaults={'unit': units}
                    )
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient_obj, amount=amount)
                return redirect('recipe', slug=recipe.slug)
        else:
            print('Form errors:', form.errors)
            return render(request, 'formChangeRecipe.html', {'form': form, 'recipe': recipe})
    else:
        form = RecipeForm(instance=recipe)

    # Получаем данные для предзаполнения ингредиентов
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    ingredients_data = []
    for ri in recipe_ingredients:
        ingredients_data.append({
            'name': ri.ingredient.name,
            'value': ri.amount,
            'units': ri.ingredient.unit
        })
    ingredients_json = json.dumps(ingredients_data)
    print('ingredients_data:', ingredients_data)  # Отладочный вывод
    print('ingredients_json:', ingredients_json)  # Отладочный вывод


    available_tags = Tag.TAG_CHOICES
    recipe_tags = recipe.tags.values_list('name', flat=True)
    context = {
        'form': form,
        'recipe': recipe,
        'recipe_tags': list(recipe_tags),
        'available_tags': available_tags,
        'ingredients_json': ingredients_json  # Передаем данные ингредиентов в шаблон
    }

    return render(request, 'formChangeRecipe.html', context)




def single_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    is_subscribed = False
    is_purchased = False
    is_favorited = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, subscribed_to=recipe.author).exists()
        is_purchased = Purchase.objects.filter(user=request.user, recipe=recipe).exists()
        is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'singlePage.html',{'recipe':recipe, 'recipe_ingredients':recipe_ingredients, 'is_subscribed':is_subscribed, 'is_purchased':is_purchased, 'is_favorited':is_favorited})


@login_required
def follows(request):
    user = request.user
    subscriptions = Subscription.objects.filter(subscriber=user).select_related('subscribed_to').order_by('-created_at')
    paginator = Paginator(subscriptions, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    subscribers_data = []
    for subscription in page.object_list:
        author= subscription.subscribed_to
        # Получаем количество рецептов подписанного пользователя
        recipe_count = author.recipes.count()
        last_recipes = author.recipes.order_by('-pub_date')[:3]
        subscribers_data.append({
            'subscription': author,
            'last_recipes': last_recipes,
            'recipe_count': recipe_count
        })

    context = {
        'page': page,
        'paginator': paginator,
        'subscribers_data': subscribers_data,
    }
    return render(request, 'myFollow.html', context)


@login_required
def shoplist(request):
    recipes = Recipe.objects.filter(buyers__user=request.user).distinct()
    context = {
        'recipes':recipes
    }
    return render(request, 'shopList.html', context)


@login_required
def download_shopping_list(request):
    ingredients = RecipeIngredient.objects.filter(
        recipe__buyers__user=request.user
    ).values(
        name=F('ingredient__name'),
        unit=F('ingredient__unit')
    ).annotate(
        total_amount=Sum('amount')
    )
    if not ingredients:
        messages.error(request, 'Ваш список покупок пуст.')
        return redirect('index')
    shopping_list = ''
    for item in ingredients:
        name = item['name']
        unit = item['unit']
        amount = item['total_amount']
        shopping_list += f'{name} ({unit}) — {amount}\n'
                
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
    return response


@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author != request.user:
        return redirect('recipe', slug=slug)
    if request.method == 'POST':
        recipe.delete()
        return redirect('index')
    return render(request, 'delete_recipe_confirm.html', {'recipe': recipe})
                    
def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)