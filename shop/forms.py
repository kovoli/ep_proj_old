from .models import Comment
from django import forms
from captcha.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(label='Проверка, что вы настоящий человек',
                             attrs={'theme': 'clean', }, required=True, )

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'positiv', 'negativ')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Введите ваш емайл'}),
            'body': forms.Textarea(attrs={'class': 'form-control ',
                                          'rows': '5'}),
            'positiv': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Ваши позитивные впечатления',
                                             'rows': '3'}),
            'negativ': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Ваши негативные впечатления',
                                             'rows': '3'})
        }
        labels = {
            'name': 'Имя',
            'body': 'Ваш отзыв',
            'positiv': 'Достоинства',
            'negativ': 'Недостатки',
        }
