# ============================================================
# AUTH MIDDLEWARE V16.9
# ============================================================

from lentra.auth.services.auth_service import AuthService


class AuthMiddleware:
    def __init__(self):
        self.auth = AuthService()

    def verify(self, request: dict):
        api_key = request.get("api_key")

        user = self.auth.validate(api_key)

        if not user:
            raise Exception("Unauthorized")

        return user
