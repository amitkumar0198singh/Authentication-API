from rest_framework.response import Response
from rest_framework import views, status
from api.models import User
from api.serializers import UserRegistrationSerializer, UserLoginSerializer
from api.auth import authenticate
from api import tokens


# Create your views here.
class UserRegistrationView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            access_token = tokens.generate_token(username, 'access', minutes=15)
            refresh_token = tokens.generate_token(username, 'refresh', days=1)
            serializer.save()
            return Response({"message": "User created successfully.", 'tokens': {'access': access_token, 'refresh': refresh_token}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                access_token = tokens.generate_token(user.username, 'access', minutes=15)
                refresh_token = tokens.generate_token(user.username, 'refresh', days=1)
                return Response({"message": "Login successful", 'tokens': {'access': access_token, 'refresh': refresh_token}}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials/User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class RefreshTokenView(views.APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if tokens.verify_token(refresh_token, 'refresh'):
            username = tokens.get_username_from_token(refresh_token)
            if username:
                new_access_token = tokens.generate_token(username, 'access', minutes=15)
                return Response({"message": "Token refreshed successfully", 'new_access_token': new_access_token}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)