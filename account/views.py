import json
import requests
import logging

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from account.models import Client
from account.permissions import IsSuperUser
from account.serializers import UserSerializer, GroupSerializer, UserAuthSerializer, ClientSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class UserAuth(generics.CreateAPIView):
    """
    View to authenticate user, throuth this view, we can access the oauth2
    endpoint to create and return a token.
    """

    logger.info("Initiate authentication user...", key="UserAuth")
    
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserAuthSerializer
    
    def post(self, request, *args, **kwargs):
        
        # validate user
        username = request.data.get("username")
        password = request.data.get("password")

        logger.info("Checking if user exists...", key="UserAuth")
        
        # check if user exists
        get_object_or_404(User, username=username)
    
        user = authenticate(username=username, password=password)
        
        if not user:
            logger.error("Authentication user failed!", key="UserAuth")
            raise PermissionDenied

        request_auth = requests.post(
            request.build_absolute_uri(reverse('oauth2_provider:token')),
            data=json.dumps(request.data)
        )

        logger.info("User authenticated successfully!", key="UserAuth")
        
        return Response(request_auth.json(), status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    """
    View to list users, accessed using `post` method all users can access this view.
    """
    
    permission_classes = [
        permissions.IsAuthenticated,
        IsSuperUser
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    View to create user, all users can access this view.
    """
    
    logger.info("Initiating user creation...")
    
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListCreateView(View):
    """
    View to receive request to access UserListView or UserCreateView.
    """
    def get(self, request):
        view = UserListView.as_view()
        return view(request)

    def post(self, request):
        view = UserCreateView.as_view()
        return view(request)


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClientCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
