from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.renderers import UserRenderer
from user.serializers import (
    UserChangePasswordSerializer,
    UserLoginSerializer,
    UserPatchSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
)


def get_tokens_for_user(user):
    """Возвращает токен и рефреш токен"""
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegisterView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """Регистрация нового пользователя"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "message": "Registration successfull"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """Логин пользователя, возвращает токены"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "message": "Login success"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"errors": ["Email or Password is not valid"]},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Профиль, информация о пользователе"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """Изменение пароля"""
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class UserLogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Выход из аккаунта, если рефреш токен найден то в черный список"""
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Enter refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = RefreshToken(refresh_token)
        if not token:
            return Response(
                {"error": "Incorrect refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token.blacklist()

        return Response(
            {"success": "Logout success"}, status=status.HTTP_200_OK
        )


class UserChangeSubscriptionView(APIView):
    permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]

    def get_object(self, pk):
        user = User.objects.filter(pk=pk).first()
        if user is not None:
            return user
        raise PermissionDenied(
            "Column not found or you don't have permission to access it"
        )

    def patch(self, request, pk):
        """Для изменения подписки пользователей, доступно только для админов"""
        user = self.get_object(pk)
        serializer = UserPatchSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
