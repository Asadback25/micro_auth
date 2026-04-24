from users.models import CustomUser
from django.db import transaction


class UserRepo:

    @staticmethod
    @transaction.atomic
    def create_user(username: str, email: str, password: str):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        user.save()
        return user
