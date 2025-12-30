from django.contrib.auth import authenticate, login, logout


class AuthenticationService:
    def authenticate(request, email, password):
        user = authenticate(request, email, password)

        if user is None:
            return None, 'Invalid credentials'

        if not user.is_active:
            return None, 'Account is inactive'

        return user, None

    def login(request, user):
        login(user)         