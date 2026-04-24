from random import randint


class OtpToken:

    @staticmethod
    def generate_otp():
        return randint(111111, 999999)
