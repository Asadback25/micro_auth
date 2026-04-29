from users.repository import UserRepo, OtpRepo
from users.tasks import EmailTask
from .OTPService import OtpToken
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


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

    @staticmethod
    def request_password_reset(email: str):
        user = UserRepo.get_by_email(email)
        if user:
            otp = OtpToken.generate_otp(email)
            EmailTask.send_verify_otp(otp, email) # For simplicity using same task

    @staticmethod
    def reset_password(email, code, new_password):
        otp = OtpRepo.get_valid_otp(email, code)
        if not otp:
            raise Exception("Invalid OTP")

        if timezone.now() > otp.created_at + timedelta(minutes=5):
            raise Exception("OTP expired")

        user = UserRepo.get_by_email(email)
        if not user:
            raise Exception("User not found")

        UserRepo.set_password(user, new_password)
        OtpRepo.mark_used(otp)