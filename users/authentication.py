import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User, LoggedOutToken


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()

        except ValueError:
            raise AuthenticationFailed('Неверный формат токена')

        if prefix.lower() != 'bearer':
            raise AuthenticationFailed('Неверный префикс токена')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен просрочен')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Невалидный токен')

        token_uid = payload.get('token_uid')
        if not token_uid:
            raise AuthenticationFailed('Отсутствует token_uid')

        if LoggedOutToken.objects.filter(token_uid=token_uid).exists():
            raise AuthenticationFailed('Токен больше недействителен. Пользователь вышел из системы')

        user_id = payload.get('user_id')
        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            raise AuthenticationFailed('Пользователь не найден')

        if not user.is_active:
            raise AuthenticationFailed('Пользователь удалён')

        return user, payload
