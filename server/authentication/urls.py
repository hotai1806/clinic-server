from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from authentication.views import UserDetails, UserList,GroupList

# router = routers.DefaultRouter()

# router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
    path('user/register/', views.UserRegister.as_view()),
]