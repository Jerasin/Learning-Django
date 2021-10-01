from django.contrib import admin
from django.urls import path , re_path , register_converter
import rest_framework 
from .api import BookListView , CreateBookView
from rest_framework import  routers 
# ใช้ตรวจสอบว่ามีสิทธิ์เข้า route นี้ไหม
from django.contrib.auth.decorators import login_required

# ใช้`from . ได้ในกรณีอยู่ใน path กับตัว app
from . import views
from .api import BookListView , CreateBookView , UpdateBookView , DeleteBookView , TestApiView


#? Book Api case use Class  viewsets.ViewSet
router_book = routers.DefaultRouter()
router_book.register(r'book/lists' , BookListView , basename="Book")
router_book.register(r'^create-book' , CreateBookView , basename="Book")
router_book.register(r'^update/book' , UpdateBookView , basename="Book")
router_book.register(r'^delete' , DeleteBookView , basename="Book")


urlpatterns = [
    #? Book Api case use Class APIView
    path('lists', TestApiView.as_view() , name='index'),
    # re_path(r'^create/book/(?P<filename>[^/]+)$', CreateBookView.as_view() , name='index'),

    # path('', views.index , name='index'),
    path('', login_required(views.BookListView.as_view() , login_url='/login') , name='index'),
    # path('detail/<slug:slug>/', views.detail , name='detail'),
    path('detail/<slug:slug>/', views.BookDetailView.as_view() , name='detail'),
    re_path(r'add/$' , views.book_add , name='book_add'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$' , views.cart_add , name='cart_add'),
    re_path(r'cart/delete/(?P<slug>[\w-]+)/$' , views.cart_delete , name='cart_delete'),
    re_path(r'card/list/' , views.cart_list , name='cart_list'),
    re_path(r'card/edit/' , views.edit_qty , name='edit_qty'),
    path('cart/checkout', views.cart_checkout , name='cart_checkout'),
    path('card/deleteall/', views.cart_delete_all , name='cart_delete_all'),
    

] 




