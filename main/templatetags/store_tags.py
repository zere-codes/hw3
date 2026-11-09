from django import template

from main.models import App

register = template.Library()


@register.filter
def stars(value):
    full = int(value)
    return '★' * full + '☆' * (5-full)

@register.filter
def reviews_count(value):
    num=str(int(value))
    if num[-1] == '1' and num[-2:] != '11':
        text=num+' '+'отзыв'
    elif (num[-1] in ('2', '3', '4')) and num[-2:] not in ('12', '13', '14'):
        text=num+' '+'отзыва'
    else:
        text=num+' '+'отзывов'
    return text

@register.filter
def count_app(value):
    num = str(int(value))
    if num[-1] == '1' and num[-2:] != '11':
        text = num + ' ' + 'приложение'
    elif (num[-1] in ('2', '3', '4')) and num[-2:] not in ('12', '13', '14'):
        text = num + ' ' + 'приложения'
    else:
        text = num + ' ' + 'приложений'
    return text

@register.filter
def category_count(value):
    num = str(int(value))
    if num[-1] == '1' and num[-2:] != '11':
        text = num + ' ' + 'категория'
    elif (num[-1] in ('2', '3', '4')) and num[-2:] not in ('12', '13', '14'):
        text = num + ' ' + 'категории'
    else:
        text = num + ' ' + 'категорий'
    return text



