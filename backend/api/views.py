from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, authentication
from rest_framework.response import Response

from api.serializers import UserSerializer, SantaUserSerializer, SantaGroupSerializer, SantaListSerializer
from .models import SantaUser, SantaGroup, SantaList


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class SantaUserViewSet(viewsets.ModelViewSet):
    serializer_class = SantaUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['group', 'list_written', 'created_at']
    search_fields = ['name', 'email', 'group__name']
    ordering_fields = ['name', 'list_written', 'created_at']
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        list_written = self.request.query_params.get('list_written')
        if list_written:
            santa_users = SantaUser.objects.filter(list_written=list_written).order_by('-created_at')
        else:
            santa_users = SantaUser.objects.all().order_by('-created_at')
        return santa_users


class SantaGroupViewSet(viewsets.ModelViewSet):
    serializer_class = SantaGroupSerializer
    filterset_fields = ['budget_limit', 'santa_day', 'created_at']
    search_fields = ['name']
    ordering_fields = ['name', 'budget_limit', 'santa_day', 'created_at']
    authentication_classes = [authentication.TokenAuthentication]

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
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return SantaList.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
