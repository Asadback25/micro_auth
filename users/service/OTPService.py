# users/service/OTPService.py

from random import randint
from django.utils import timezone
from datetime import timedelta
from users.repository import OtpRepo
from users.repository import UserRepo

class OtpToken:

    @staticmethod
    def generate_otp(email: str):
        code = str(randint(100000, 999999))

        OtpRepo.create(email, code)

        return code

    # users/service/otp_service.py

    @staticmethod
    def verify(email, code):

        otp = OtpRepo.get_valid_otp(email, code)

        if not otp:
            raise Exception("Invalid OTP")

        if timezone.now() > otp.created_at + timedelta(minutes=5):
            raise Exception("OTP expired")

        OtpRepo.mark_used(otp)

        user = UserRepo.get_by_email(email)

        if not user:
            raise Exception("User not found")

        UserRepo.activate_user(user)



