from django.contrib import admin
from django.urls import path , re_path
from . import views
# ใช้`from . ได้ในกรณีอยู่ใน path กับตัว app

urlpatterns = [
    path('index/<int:id>', views.index , name='index'),
    path('hello/<int:id>', views.hello , name='hello'),
    re_path(r'article/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$', views.article , name='article'),
]

#  ใช้กับ Search Engie
# re_path(r'article/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$', views.article),