from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationService:
    def authenticate(request, email, password):
        user = authenticate(request, email, password)

        if user is None:
            return None, "Invalid credentials"

        if not user.is_active:
            return None, "Account is inactive"

        return user, None

    def login(request, user):
        login(user)


class UserService:

    @staticmethod
    def withdraw(user_id, amount):
        if amount < 1:
            return False, "Invalid amount value"

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"

        if amount > user.balance:
            return False, "Not enough money on user's balance"

        user.balance -= amount
        user.save()
        return True, f"Withdraw completed successfully. {amount=}"

    @staticmethod
    def deposit(user_id, amount):
        if amount < 1:
            return False, "Invalid amount value"

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"
        except Exception as e:
            print(e)
            return False, "Something went wrong"

        user.balance += amount
        user.save()
        return True, f"Deposit completed successfully. {amount=}"
