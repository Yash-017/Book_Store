
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from authentication.emails import send_otp,send_mail

from .decorators import redirect_if_no_files
from .models import Book, Topic,Nuser,UploadedFile
from .forms import BookForm,UploadedFileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .forms import NuserCreationForm

from django.views.decorators.csrf import csrf_exempt


#
from django.contrib.auth import get_user_model
User=get_user_model

# Create your views here.

# all_books =[
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design thinking'},
#     {'id': 3, 'name': 'First Principles'},
#     {'id': 4, 'name': "Can't hurt me"},
#     {'id': 5, 'name': 'Meditations'},
# ]


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' :
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exists')

        user = authenticate(request, username=username, password=password)   

        if user is not None:
            login(request, user)
            return redirect('book-list')
        
        else:
            messages.error(request, 'Username and Password does not match')



    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def loginPage2(request):
    page='login_2'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' :
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exists')

        user = authenticate(request, username=username, password=password)   

        if user is not None:
            login(request, user)
            return redirect('data-list')
        
        else:
            messages.error(request, 'Username and Password does not match')



    context = {'page':page}
    return render(request, 'base/login_2.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #so that we have the form instance thats why commit = False
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html',{'form':form})

def registerPage2(request):   
    if request.method == 'POST':
        form = NuserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('home')
    else:
        form = NuserCreationForm()

    return render(request, 'base/register.html', {'form': form})

def home(request):
    all_books=Book.objects.all()
    topic=Topic.objects.all()
    context = {'books':all_books}
    return render(request, 'base/home.html', context)

def bookList(request):    
    all_books=Book.objects.all()
    topic=Topic.objects.all()
    context = {'books':all_books}
    return render(request,'base/book_list.html',context)

def dataList(request):    
    all_books=Book.objects.all()
    topic=Topic.objects.all()
    context = {'books':all_books}
    return render(request,'base/data_list.html',context)

def books(request,pk):
    # book_name = None
    # for i in all_books:
    #     if i ['id'] == int(pk):
    #         book_name=i

    book_name = Book.objects.get(id=pk)
    context = {'book_key':book_name}
    return render(request,'base/books.html',context)


@login_required(login_url='/login_2')
def createBook(request):
    form = BookForm()

    #see request in detail
    if request.method == "POST" :
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        print(request.POST)
    context = {'form' : form}
    return render(request, 'base/book_form.html',context)


@login_required(login_url='/login_2')
#update_book

def updateBook(request, pk):
    
    book = Book.objects.get(id=pk)
    #instance/initial
    form = BookForm(instance=book)

    if request.user != book.host:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        form=BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form': form}
    
    return render(request, 'base/book_form.html', context)

# def deleteBook(request,pk):

#     book = Book.objects.get(id=pk)

#     form = changes in forms.py etc
    
#     context = {'form' : form}

#     return render (request, 'base/delete_fomr.html', context)

@login_required(login_url='/login_2')
def deleteBook(request,pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        #delete method
        book.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'obj' : book})



def user_list(request):
    authors = Nuser.objects.filter(is_author=True, public_visibility=True)
    sellers = Nuser.objects.filter(is_seller=True, public_visibility=True)

    return render(request, 'base/auth_sell.html', {'authors': authors, 'sellers': sellers})




@login_required(login_url='/login_2')
def upload_books(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('uploaded_files')
    else:
        form = UploadedFileForm()

    return render(request, 'base/upload_books.html', {'form': form})

@login_required(login_url='/login_2')
@redirect_if_no_files
def uploaded_files(request):
    files = UploadedFile.objects.filter(user=request.user, visibility=True)
    return render(request, 'base/uploaded_files.html', {'files': files})





###########################################################################################
###########################################################################################
################################ JWT VIEWS ################################################
from rest_framework.response import Response
from authentication.serializers import UploadedFileSerializer, UserRegistraionSerializer,UserLoginSerializer, UserProfileSerializer,UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from authentication.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
#jwt
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(Nuser):
    refresh = RefreshToken.for_user(Nuser)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format = None):
        serializer= UserRegistraionSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.username = serializer.email
            Nuser = serializer.save()
            token = get_tokens_for_user(Nuser)
            return Response({'msg':'Registration successful'},
            status=status.HTTP_201_CREATED)  
        print(serializer.errors)           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request,format = None):
        serializer= UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            Nuser=authenticate(email=email, password=password)
            if Nuser is not None: 
                token = get_tokens_for_user(Nuser) 
                return Response({'token':token,'msg':'Login successful'},
                status=status.HTTP_200_OK)  
            else:
                return Response({'erros':{'non-field-error':['email or password not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileView(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    #print("111111")
    def get(self,request):
        print("22222")
        print(request.user.id)
        serializer = UserProfileSerializer(request.user)
        data = {}

        data['email'] = request.user.email
        data['id'] = request.user.id
        return JsonResponse(data, status.HTTP_200_OK)
    
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
class RegisterAPI(APIView):
   
    authentication_classes = [SessionAuthentication]  # Use SessionAuthentication for CSRF protection
    permission_classes = [IsAuthenticated]  # Use IsAuthenticated permission, adjust as needed
    def post(self,request):
        try:
            data=request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                return Response({
                    'status':200,
                    'message':"success check email",
                    'data':serializer.data,
                })

            return Response({
                'status':400,
                'message':"something went wrong",
                'data':serializer.errors,
            })
        except Exception as e:
            print(e)

# views.py


from .forms import OTPVerificationForm

def generate_otp(request):
    user = request.user
    if user.is_authenticated:
        otp_value = user.generate_otp()
        return render(request, 'generate_otp.html', {'otp_value': otp_value})
    else:
        return redirect('login')

def verify_otp(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = OTPVerificationForm(request.POST)
            if form.is_valid():
                otp_value = form.cleaned_data['otp']
                if user.verify_otp(otp_value):
                    user.is_verified = True
                    user.save()
                    return redirect('home')
                else:
                    # Handle invalid OTP (e.g., show error message)
                    pass
        else:
            form = OTPVerificationForm()
        return render(request, 'base/email.html', {'form': form})
    else:
        return redirect('login')


class UploadedFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        files = UploadedFile.objects.filter(user=request.user)
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)