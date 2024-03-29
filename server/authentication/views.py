import json
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth.models import Group
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin

from authentication.models import User
from authentication.serializers import UserSerializer, GroupSerializer, RegisterSerializer
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Create your views here.

# Create the API views


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user_group = self.request.query_params.get('user_group', None)
        print(user_group)
        if user_group is None:
            return User.objects.all()
        return User.objects.filter(groups__name__in=[user_group])


class UserDetails(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    permission_classes = [permissions.AllowAny]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserRegister(OAuthLibMixin, APIView):
    permission_classes = [permissions.AllowAny]

    serializers_class = RegisterSerializer
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None and request.data != {}:
            data = request.data

            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    user = serializer.save()

                    return Response(data={"message": "create account success"}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=str(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "You are not authorized to access this resource"})


@api_view(['GET'])
def get_current_role(request):
    try:
        get_current_account_id = request.META['current_account_id']
        get_current_user = User.objects.get(id=get_current_account_id)
        full_name = get_current_user.first_name + ' ' + get_current_user.last_name
        get_current_user_role = get_current_user.groups.all().values_list('name', flat=True)
        data = [i for i in get_current_user_role]
        print(full_name)
        return Response(data={"roles": data, "full_name":full_name}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
