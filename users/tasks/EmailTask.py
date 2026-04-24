from django.core.mail import send_mail
from django.conf import settings

class EmailTask:
    @staticmethod
    def send_verify_otp(otp, email):
        send_mail(
            subject='OTP Verification',
            message=f'Your OTP is {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )