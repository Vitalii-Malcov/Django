from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Сначала обычная проверка заголовка Authorization: Bearer
        result = super().authenticate(request)
        if result is not None:
            return result
        # Если заголовка нет, берём access-токен из cookie
        raw = request.COOKIES.get('access_token')
        if raw is None:
            return None
        validated_token = self.get_validated_token(raw)
        return self.get_user(validated_token), validated_token
