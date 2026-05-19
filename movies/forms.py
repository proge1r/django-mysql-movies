from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'description', 'rating', 'image', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'genres': forms.CheckboxSelectMultiple(),
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': '1.0', 'max': '10.0', 'placeholder': 'e.g. 8.5'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
        }