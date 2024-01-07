from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import Book, Topic, Message, Nuser

class CustomUserAdmin(UserAdmin):
    model = Nuser
    list_display = ['email','name','id', 'public_visibility', 'is_author', 'is_seller', 'is_active']
    ordering = ['name'] 

admin.site.register(Book)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Nuser, CustomUserAdmin)

