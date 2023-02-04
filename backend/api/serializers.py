from django.contrib.auth.models import User
from rest_framework import serializers

from .models import SantaUser, SantaGroup, SantaList


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SantaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SantaUser
        fields = [
            'id',
            'name',
            'email',
            'group',
            'secret_santa',
            'list_written',
            'created_at'
        ]
        read_only_fields = ['id', 'group', 'secret_santa', 'list_written', 'created_at']


class SantaGroupSerializer(serializers.ModelSerializer):
    santa_users = SantaUserSerializer(many=True)

    class Meta:
        model = SantaGroup
        fields = [
            'id',
            'name',
            'budget_limit',
            'santa_day',
            'created_at',
            'santa_users'
        ]
        read_only_fields = ['id', 'created_at']


class SantaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SantaList
        fields = [
            'santa_user',
            'text',
            'created_at'
        ]
