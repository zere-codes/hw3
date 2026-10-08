from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Review, App


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['username', 'comment', 'stars', 'recommended']

        labels={
            'username':'Имя',
            'comment':'комментарий о приложении ',
            'stars':'оценка',
            'recommended':'рекомендуете?',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Как вас зовут?',
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Что вы думаете о приложении?',
            }),
            'stars': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
            }),
        }

    def clean(self):
        recommended=self.cleaned_data.get('recommended')
        stars = self.cleaned_data.get('stars')
        comment=self.cleaned_data.get('comment')

        if stars is not None and stars < 3 and recommended == 'да':
            raise forms.ValidationError(
                'Вы не можете рекомендовать приложение если оценили его меньше 3 из 5'
            )
        if len(comment)>600:
            raise forms.ValidationError('Комментарий не может превышать 600 символов')

    def clean_stars(self):
        stars = self.cleaned_data.get('stars')

        if stars is None:
            raise forms.ValidationError('Введите оценку')

        if stars < 1 or stars > 5:
            raise forms.ValidationError(
                'Оценка должна быть от 1 до 5.'
            )
        return stars

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'description', 'price', 'weight_kb', 'category', 'icon']
        labels = {
            'name': 'название',
            'description': 'описание ',
            'price': 'цена',
            'weight_kb': 'размер',
            'category': 'категория',
            'icon': 'картинка',
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label='Имя'
        self.fields['email'].label='email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Уже есть пользователь с такой почтой')
        return email



