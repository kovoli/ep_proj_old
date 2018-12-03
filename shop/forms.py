from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(label='Проверка ')

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Введите ваш емайл'}),
            'body': forms.Textarea(attrs={'class': 'form-control ',
                                          'rows': '5'}),
            'captcha': ReCaptchaField(label='Проверка ', error_messages={'required': 'fgsdgsfg'})

        }
        labels = {
            'name': 'Имя',
            'body': 'Ваш отзыв',
        }
