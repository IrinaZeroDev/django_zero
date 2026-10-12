from django.forms import ModelForm, Textarea, TextInput

from .models import Film


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'description', 'review']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например, «Иван Васильевич меняет профессию»',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'О чём фильм',
            }),
            'review': Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваши впечатления',
            }),
        }
