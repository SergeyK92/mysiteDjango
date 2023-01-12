from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import Women, Category

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]


# menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    # posts это имя списка (листа) содержащего строчки модели Women
    context_object_name = 'posts'
    cats = Category.objects.all()

    # Функция для определения контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница сайта'
        context['cat_selected'] = 0,
        return context

    # Указываем что именно выбирать из модели Women
    def get_queryset(self):
        return Women.objects.filter(is_published=True).order_by('-time_update')


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts[::-1],
#         'menu': menu,
#         'title': 'Главная страница сайта',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'ABOUTстраница сайта', 'menu': menu})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # Указываем путь по которому перенаправляем страницу после загрузки формы
    # Можно не указывать, тогда сработает метод     def get_absolute_url(self): модель women
    success_url = reverse_lazy('home')


    ## В template для вывода полей формы используется имя form
    # его можно переопределить в get_context_data например context['form_1'] = self.form_class

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        # context['form_1'] = self.form_class

        # print(context)

        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         # print(form.cleaned_data)
#         if form.is_valid():
#             form.save()  # Используется при связи формы с моделями в БД.
#             return redirect('home')
#             # try:
#             #     # Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи', 'menu': menu})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Регистрация и вход пользователей')


# Класс для отображения отдельного поста
class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    # Здесь post  - это имя строчки (объект) базы данных. Когда мы ее пытаемся вывести, срабатывает
    # магический метод str который мы в классе Women переопределили. от выводит поле title модели women

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        # print(context)

        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    # posts это имя списка (листа) содержащего строчки модели Women
    context_object_name = 'posts'
    # Генерация исключения в случае ошибки, например пытаемся обратится по слагу которого нет, \
    # или нет записей в БД
    allow_empty = False

    # Функция для определения контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context

    # Указываем что именно выбирать из модели Women
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).order_by('-time_update')


# def show_category(request, cat_slug):
#     cat = get_object_or_404(Category, slug=cat_slug)
#     # print(type(cat), cat.id)
#     posts = Women.objects.filter(cat=cat.pk)
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat.id,
#     }
#     return render(request, 'women/index.html', context=context)


def categories(request, cat_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1> Статьи по категориям </h1> <p> Номер id {cat_id} </p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>страница не найдена 404 </h1>')
