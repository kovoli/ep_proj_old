from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': 'Введите ваш емайл'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})

        }
        labels = {
            'name': 'Имя',
            'body': 'Ваш отзыв'
        }
