from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BlockedUserJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        if user.is_blocked:
            raise AuthenticationFailed(
                "Your account has been blocked."
            )

        return user