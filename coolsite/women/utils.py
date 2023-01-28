from django.db.models import Count

from women.models import Category

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        menu_user = menu.copy()
        context = kwargs
        # cats = Category.objects.all()
        cats = Category.objects.annotate(total=Count('women')).filter(total__gt=0, women__is_published=True)

        if not self.request.user.is_authenticated:
            menu_user.pop(1)
        context['menu'] = menu_user
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
