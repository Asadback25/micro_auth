from users.api.v1 import RegisterSerializer
from users.service import UserService
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


