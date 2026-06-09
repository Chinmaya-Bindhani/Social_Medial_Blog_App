from django import forms
from django.contrib.auth.forms import UserCreationForm
from secondapp.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model = User
        fields=['username','email','password1','password2']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']

class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']