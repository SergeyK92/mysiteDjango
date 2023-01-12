from django import forms
from django.core.exceptions import ValidationError


from .models import *

# Создание отдельной формы
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок',
#                             widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label='URL')
#     photo = forms.ImageField(label='Фото')
#     text = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 10}), label='Контент')
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
#                                  empty_label='Категория не выбрана')

# Создание формы связанной с моделями
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'text', 'photo', 'is_published', 'cat']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'text': forms.Textarea(attrs={'cols': 90, 'rows': 10})
                   }

    # Метод для валидации поля title
    def clean_title(self):
        # получение данных из поля title
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина заголовка превышает 100 символов')
        return title
