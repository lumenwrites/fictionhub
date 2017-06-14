from django.forms import ModelForm
from django import forms

from .models import Series


class SeriesForm(ModelForm):
    class Meta:
        model = Series
        fields = ['title', 'free_chapters', 'price'] 
