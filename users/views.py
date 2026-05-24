from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.authentication import JWTAuthentication
from users.models import LoggedOutToken
from users.serializers import RegisterUserSerializer, UpdateUserSerializer, LoginUserSerializer
from users.services import generate_token


class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            data={'id': user.id, 'email': user.email},
            status=status.HTTP_201_CREATED
        )


class UpdateUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        serializer = UpdateUserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        return Response(
            data={'id': updated_user.id, 'email': updated_user.email, 'name': updated_user.name},
            status=status.HTTP_200_OK
        )


class LoginUserAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = generate_token(user)

        return Response(data={'token': token}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            data={
                'id': request.user.id,
                'email': request.user.email,
                'name': request.user.name,
                'role': request.user.role.name if request.user.role else None
            },
            status=status.HTTP_200_OK
        )


class DeleteUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return Response(data={'detail': 'Пользователь удалён'}, status=status.HTTP_200_OK)


class LogoutUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token_uid = request.auth['token_uid']
        LoggedOutToken.objects.get_or_create(token_uid=token_uid)

        return Response(
            data={'detail': 'Пользователь вышел из системы. Токен больше недействителен.'},
            status=status.HTTP_200_OK
        )
