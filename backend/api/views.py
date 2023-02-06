from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, views, permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.serializers import UserSerializer, SantaUserSerializer, SantaGroupSerializer, SantaListSerializer
from api.jwt import JWTAuthentication
from api.models import SantaUser, SantaGroup, SantaList
from backend.settings import SECRET_KEY

import jwt
import datetime


class LoginView(views.APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return Response({'Error': "Please provide username/password"}, status="400")

        user = authenticate(username=username, password=password)
        if user:
            payload = {
                "username": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }
            jwt_token = {
                "token": jwt.encode(payload, SECRET_KEY),
                "token_type": "Bearer"
            }
            return Response(jwt_token, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
            )
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class SantaUserViewSet(viewsets.ModelViewSet):
    serializer_class = SantaUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['group', 'list_written', 'created_at']
    search_fields = ['name', 'email', 'group__name']
    ordering_fields = ['name', 'list_written', 'created_at']
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return SantaUser.objects.all().order_by('-created_at')


class SantaGroupViewSet(viewsets.ModelViewSet):
    serializer_class = SantaGroupSerializer
    filterset_fields = ['budget_limit', 'santa_day', 'created_at']
    search_fields = ['name']
    ordering_fields = ['name', 'budget_limit', 'santa_day', 'created_at']
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return SantaGroup.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        santa_users = request.data.get("santa_users")
        del request.data["santa_users"]

        instance = SantaGroup.objects.create(
            name=request.data.get('name'),
            budget_limit=request.data.get('budget_limit'),
            santa_day=request.data.get('santa_day'),
        )

        for user in santa_users:
            santa_user = SantaUser.objects.create(**user)
            instance.santa_users.add(santa_user)
        instance.save()

        serializer = SantaGroupSerializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SantaListViewSet(viewsets.ModelViewSet):
    serializer_class = SantaListSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return SantaList.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        santa_user = SantaUser.objects.get(id=request.query_params.get('santa_user'))
        if santa_user:
            instance = SantaList.objects.create(
                santa_user=santa_user,
                text=request.data.get('text'),
            )
            serializer = SantaListSerializer(instance, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
