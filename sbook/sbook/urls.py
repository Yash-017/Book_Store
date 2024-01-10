
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import RegisterAPI



    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authentication.urls')),
    path('api/user/', include('authentication.urls')),
    #path('register_two/',RegisterAPI.as_view()),
    
    
    
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
