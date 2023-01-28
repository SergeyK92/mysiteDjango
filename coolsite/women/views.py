from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import Women, Category
from .utils import DataMixin, menu


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    # posts это имя списка (листа) содержащего строчки модели Women
    context_object_name = 'posts'

    # Функция для переопределения контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # с_def это словарь контектса
        c_def = self.get_user_context(title='Главная страница сайта')
        context.update(c_def)
        return context

    # Указываем что именно выбирать из модели Women
    def get_queryset(self):
        return Women.objects.filter(is_published=True).order_by('time_update').select_related('cat')


def about(request):
    cats = Category.objects.all()
    return render(request, 'women/about.html', {'title': 'ABOUTстраница сайта', 'menu': menu, 'cats': cats})


# Добавление записи на сайт
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # Указываем путь по которому перенаправляем страницу после загрузки формы
    # Можно не указывать, тогда сработает метод  def get_absolute_url(self): модель women
    success_url = reverse_lazy('home')
    # Указывает адрес перенаправления для незарегистрированных пользователей
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи',
                                      cat_selected=None)
        context.update(c_def)
        # context['form_1'] = self.form_class
        return context


def contact(request):
    return HttpResponse('Обратная связь')


def register(request):
    return HttpResponse('Регистрация пользователей')


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
        c_def = self.get_user_context(title=context['post'],
                                      cat_selected=None)
        context.update(c_def)
        return context


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    # posts это имя списка (листа) содержащего строчки модели Women
    context_object_name = 'posts'
    # Генерация исключения в случае ошибки, например пытаемся обратится по слагу которого нет, \
    # или нет записей в БД
    allow_empty = False

    # Указываем что именно выбирать из модели Women
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).order_by(
            '-time_update').select_related('cat')

    # Функция для определения контекста

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        context.update(c_def)
        return context


def categories(request, cat_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1> Статьи по категориям </h1> <p> Номер id {cat_id} </p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>страница не найдена 404 </h1>')


# Класс для регистрации пользователей
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context.update(c_def)
        return context

    # Метод для автоматического входа в систему
    # при успешной регистрации пользователя
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# Класс для авторизации пользователей
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context.update(c_def)
        return context

    # Метод вызывается при успешной авторизации пользователя
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
