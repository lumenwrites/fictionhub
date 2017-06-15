from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email'    : forms.TextInput(attrs = {'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password2')
        
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'website', 'about', 'avatar','background'] #'email_subscriptions', 'email_comments'
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Username'}),
            'email'    : forms.TextInput(attrs = {'placeholder': 'Email'}),
        }
    
