from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from authentication.views import UserDetails, UserList,GroupList, get_current_role

# router = routers.DefaultRouter()

# router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns = [
    path('users', UserList.as_view()),
    path('users/<pk>', UserDetails.as_view()),
    path('groups', GroupList.as_view()),
    path('user/register', views.UserRegister.as_view()),
    path('role',get_current_role),
]