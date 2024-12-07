from .models import Purchase

def shopping_list_count(request):
    if request.user.is_authenticated:
        count = Purchase.objects.filter(user=request.user).count()
    else:
        count = 0  # Или какое-то другое значение по умолчанию
    return {'shopping_list_count': count}