from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'description', 'rating', 'image']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }