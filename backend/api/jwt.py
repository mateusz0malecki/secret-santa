from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions

from django.conf import settings
from django.contrib.auth.models import User

import jwt


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        if not auth_header:
            raise exceptions.AuthenticationFailed('Not authenticated.')
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(' ')

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid')
        token = auth_token[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            username = payload['username']
            user = User.objects.get(username=username)
            return user, token
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired. Please login again.')
        except jwt.DecodeError or jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token not valid.')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist.')
