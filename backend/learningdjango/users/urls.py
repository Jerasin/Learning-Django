from rest_framework import  routers 
from .api import CustomUserCreate , UserListView , UserView , UserUpdateView , UserDeleteView

router_users = routers.DefaultRouter()
router_users.register(r'register' , CustomUserCreate , basename="User")
router_users.register(r'users' , UserListView , basename="User")
router_users.register(r'user' , UserView , basename="User")
router_users.register(r'update/user' , UserUpdateView , basename="User")
router_users.register(r'delete/user' , UserDeleteView , basename="User")