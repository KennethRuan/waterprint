from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class WaterUsageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('water_usage',)

class AddFriendsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('friends',)