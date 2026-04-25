from users.repository import UserRepo
from users.tasks import EmailTask
from .OTPService import OtpToken
from django.db import transaction


class UserService:
    @staticmethod
    def register_user(username: str, email: str, password: str):
        UserRepo.create_user(
            username=username,
            email=email,
            password=password
        )
        otp = OtpToken.generate_otp(email)
        transaction.on_commit(lambda: EmailTask.send_verify_otp(otp, email))