from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import Women, Category
from .utils import DataMixin, menu


# menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    # posts это имя списка (листа) содержащего строчки модели Women
    context_object_name = 'posts'

    # Функция для определения контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # с_def это словарь контектса
        c_def = self.get_user_context(title='Главная страница сайта')
        context.update(c_def)
        return context

    # Указываем что именно выбирать из модели Women
    def get_queryset(self):
        return Women.objects.filter(is_published=True).order_by('-time_update')


def about(request):
    cats = Category.objects.all()
    return render(request, 'women/about.html', {'title': 'ABOUTстраница сайта', 'menu': menu, 'cats': cats})


# Добавление записи на сайт
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # Указываем путь по которому перенаправляем страницу после загрузки формы
    # Можно не указывать, тогда сработает метод     def get_absolute_url(self): модель women
    success_url = reverse_lazy('home')
    #Указывает адрес перенаправления для незарегистрированных пользователей
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context.update(c_def)
        # context['form_1'] = self.form_class
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
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    # pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['post'] - хранится объект базы данных, и когда вы его вызывает на печать работает магический метод str
        c_def = self.get_user_context(title=context['post'])
        context.update(c_def)
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


class WomenCategory(DataMixin, ListView):
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
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        context.update(c_def)
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
