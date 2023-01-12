menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]

class DataMixin:

    def get_context_data(self, **kwargs):
        context = kwargs
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница сайта'
        context['cat_selected'] = 0
        return context