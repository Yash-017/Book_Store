from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Book
from .models import Nuser
from .models import UploadedFile

class BookForm(ModelForm):
    class Meta:
        model=Book
        fields = '__all__'

# class LoginForm(ModelForm):
#     class Meta:
#         model=Nuser
#         fields = '__all__'

from django import forms

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class NuserCreationForm(UserCreationForm):
    class Meta:
        model = Nuser
        fields = ['username', 'email', 'password1', 'password2', 'name', 'public_visibility', 'is_author', 'is_seller', 'birthyear', 'address']


class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'visibility', 'cost', 'year_of_published', 'file']


        