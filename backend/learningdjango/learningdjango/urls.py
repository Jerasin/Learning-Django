"""learningdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path , include 
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from book.urls import router_book
from users.urls import router_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('myapp.urls','myapp') , namespace='myapp')),

    #? Book Api
    path('api-book/',include(('book.urls','book_api') , namespace='book_api')),

    #? Token Api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #? User Api
    # path('api-users/',include(('users.urls','users') , namespace='users')),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
#  ใช้กับ Search Engie

urlpatterns += router_book.urls 
urlpatterns += router_users.urls 