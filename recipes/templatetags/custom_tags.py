from django import template

register = template.Library()

@register.filter(name='ru_pluralize')
def ru_pluralize(value, arg="рецепт,рецепта,рецептов"):
    args = arg.split(',')
    variants = {
        'one': args[0],
        'few': args[1],
        'many': args[2],
    }
    number = abs(int(value))
    if number % 10 == 1 and number % 100 != 11:
        form = variants['one']
    elif 2 <= number % 10 <= 4 and not 12 <= number % 100 <= 14:
        form = variants['few']
    else:
        form = variants['many']
    return f"{value} {form}"
    