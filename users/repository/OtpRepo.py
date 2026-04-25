# users/repository/otp_repo.py

from users.models import OTP

class OtpRepo:

    @staticmethod
    def create(email: str, code: str):
        return OTP.objects.create(
            email=email,
            code=code
        )

    @staticmethod
    def get_latest(email: str, code: str):
        return OTP.objects.filter(
            email=email,
            code=code,
            is_used=False
        ).order_by('-created_at').first()

    @staticmethod
    def get_valid_otp(email, code):
        return OTP.objects.filter(
            email=email,
            code=code,
            is_used=False
        ).order_by('-created_at').first()

    @staticmethod
    def mark_used(otp):
        otp.is_used = True
        otp.save()