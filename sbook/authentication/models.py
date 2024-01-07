from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission,AbstractUser
from django.utils import timezone
from datetime import datetime

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None,**other_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, name, password, **other_fields)

    



class Nuser(AbstractUser):
    email = models.EmailField(verbose_name = 'Email',max_length=255,unique=True)
    name = models.CharField(max_length=150, unique=True)    
    public_visibility = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    birthyear = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    

    def __str__(self):
        return self.email

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name 

#Main Book Parent
class Book(models.Model):
    #host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    host = models.ForeignKey('authentication.Nuser', on_delete=models.SET_NULL, null=True)
    topic =models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    #if topic is below book class then
    # topic =models.ForeignKey('Topic', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    # Null is Allowed
    description = models.TextField(null=True, blank=True)
    #Authors = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name

# User who takes Books
class Message(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.Nuser', on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    body = models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    


    

# 1) (create a page "Authors and Sellers" tab where you fetch certain users registered on platform. 
# 2) "public_visibility" (boolean field) while registering.

# 1) (40-80min) use custom user model with inheriting ""AbstractUser"" class or 
#""AbstractBaseUser"" class

# add more parameters to custom user model like ""public_visibility""(boolean value)
    #age(auto calculated while creating object), birth year,address etc. "


# create "uploaded_files" model with relvent parameters that supports this feature.
# once file is uploaded user is able to view existing uploaded file in his "uploaded files" section of dashboard.
# collect meta data details like title of book/file , description, visibility , cost , year of published



class UploadedFile(models.Model):
    user = models.ForeignKey('authentication.Nuser', on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_of_published = models.PositiveIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/')