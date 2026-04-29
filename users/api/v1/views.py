from users.api.v1.serializers import (
    RegisterSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from users.service import UserService, OtpToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterApiView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                UserService.register_user(username, email, password)
                return Response(status=status.HTTP_201_CREATED, data={'message': 'User registered successfully. Please verify your email.'})
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': str(e)})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


# users/api/v1/views.py


class VerifyOtpView(APIView):

    def post(self, request):
        try:
            OtpToken.verify(
                request.data.get('email'),
                request.data.get('code')
            )
            return Response({"message": "Verified"})

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                if not user.is_active:
                    return Response({"error": "User is not active"}, status=status.HTTP_401_UNAUTHORIZED)

                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            UserService.request_password_reset(serializer.validated_data['email'])
            return Response({"message": "If an account with this email exists, a password reset OTP has been sent."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                UserService.reset_password(
                    serializer.validated_data['email'],
                    serializer.validated_data['code'],
                    serializer.validated_data['new_password']
                )
                return Response({"message": "Password reset successful"})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)