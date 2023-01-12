from django.db import models

# Create your models here.
from django.urls import reverse


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True, verbose_name='URL')
    text = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликованность')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')


    def __str__(self):
        return self.title

    # метод для формирования URL адреса для конкретного объекта в таблице
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Класс для правильного отображания модели в админ-панели
    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['time_create', 'title']


#
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.CharField(max_length=255, null=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # Класс для правильного отображания модеои в админ-панели
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id', 'name']
