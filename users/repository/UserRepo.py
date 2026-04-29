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

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def activate_user(user):
        user.is_active = True
        user.save()

    @staticmethod
    def set_password(user, password):
        user.set_password(password)
        user.save()
