from django import template
from women.models import Women, Category

# Для регистрации собственных шаблонных тегов
# необходимо создать экземпляр класса Library
register = template.Library()


# Функция для работы простого тега
# Возвращает коллекцию
# @register.simple_tag(name='get_cats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)
#
#
# # Функция для работы включающего тега
# # возвращает фрагмент html страницу
# @register.inclusion_tag('women/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)
#     return {'cats': cats, 'cat_selected': cat_selected}
