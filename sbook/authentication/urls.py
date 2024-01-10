from django.urls import path
from . import views
from authentication.views import RegisterAPI, UploadedFilesView, UserLoginView, UserRegistrationView,UserProfileView




urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('login_2/',views.loginPage2,name="login_2"),

    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('login_2/reg_f/', views.registerPage2, name="reg_f"),

    path('',views.home, name="home"),
    path('books/<str:pk>/', views.books, name="books"),
    
    path('create-book/', views.createBook, name="create-book"),
    path('update-book/<str:pk>/', views.updateBook, name="update-book"),
    path('delete-book/<str:pk>/', views.deleteBook, name="delete-book"),
    path('book_list/', views.bookList, name="book-list"),
    path('data_list/', views.dataList, name="data-list"),
    
    path('auth_sell/', views.user_list , name='auth_sell'),
    path('upload_books/', views.upload_books, name='upload_books'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    #path('generate_otp/', views.send_email, name='generate_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    

    ##########################################################################

    path('registerjwt/', UserRegistrationView.as_view(), name = 'jwtreg'),
    path('loginjwt/', UserLoginView.as_view(), name = 'jwtlog'),
    path('profilejwt/', UserProfileView.as_view(), name = 'profile'),
    path('uploaded-files/', UploadedFilesView.as_view(), name='uploaded-files'),
    #path('register_twofac/', RegisterAPI.as_view(),name='register-api'),
    



    
    

]



   