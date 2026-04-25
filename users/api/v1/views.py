from users.api.v1 import RegisterSerializer
from users.service import UserService, OtpToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterApiView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            UserService.register_user(username, email, password)
            return Response(status=status.HTTP_201_CREATED, data={'message': 'User registered successfully'})
        return Response(status=status.HTTP_400_BAD_REQUEST)


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