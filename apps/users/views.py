from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import LoginSerializer, RegisterSerializer


def set_auth_cookies(response, access, refresh):
    # secure=False для разработки, на продакшене нужен True (и HTTPS)
    response.set_cookie(
        'access_token', access, httponly=True, samesite='Lax', secure=False,
        max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
    )
    response.set_cookie(
        'refresh_token', refresh, httponly=True, samesite='Lax', secure=False,
        max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
    )


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response = Response({'message': 'Вход выполнен', 'access': str(access), 'refresh': str(refresh)})
        set_auth_cookies(response, str(access), str(refresh))
        return response


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # refresh берём из cookie, если его нет, то из тела запроса
        raw = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        if not raw:
            return Response({'detail': 'Refresh-токен не передан'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TokenRefreshSerializer(data={'refresh': raw})
        try:
            serializer.is_valid(raise_exception=True)
        except (InvalidToken, TokenError):
            return Response({'detail': 'Токен недействителен или истёк'}, status=status.HTTP_401_UNAUTHORIZED)

        access = serializer.validated_data['access']
        # из-за ROTATE_REFRESH_TOKENS приходит и новый refresh
        refresh = serializer.validated_data['refresh']
        response = Response({'access': access})
        set_auth_cookies(response, access, refresh)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        raw = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        if not raw:
            return Response({'detail': 'Refresh-токен не передан'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(raw).blacklist()
        except TokenError:
            return Response({'detail': 'Токен недействителен'}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Выход выполнен'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
