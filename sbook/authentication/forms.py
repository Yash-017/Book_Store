from django.forms import ModelForm

from .models import Book
from .models import Nuser
from .models import UploadedFile

class BookForm(ModelForm):
    class Meta:
        model=Book
        fields = '__all__'

class LoginForm(ModelForm):
    class Meta:
        model=Nuser
        fields = '__all__'




class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'visibility', 'cost', 'year_of_published', 'file']


        