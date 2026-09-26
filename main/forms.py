from django import forms
from .models import Review

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
        stars=self.cleaned_data['stars']
        recommended=self.cleaned_data['recommended']
        comment=self.cleaned_data['comment']
        if stars<=0 or stars>5:
            raise forms.ValidationError('Оценка должна быть от 1 до 5.')
        if stars<3 and recommended=='да':
            raise forms.ValidationError('Вы не можете рекомендовать приложение если оценили его меньше 3 из 5 ')
        if len(comment)>600:
            raise forms.ValidationError('Комментарий не может превышать 600 символов')


