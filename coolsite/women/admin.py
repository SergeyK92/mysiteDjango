from django.contrib import admin
from .models import *


# Register your models here.
# Класс для отображения информации в админ панели
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_editable = ('is_published', )
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}

# Класс для отображения информации в админ панели
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)

admin.site.register(Category, CategoryAdmin)
