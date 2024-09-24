from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from rest_framework.authentication import TokenAuthentication


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                token, _ = Token.objects.get_or_create(user=user)  # Create a token for the new user
                return Response({
                    "success": "User created successfully",
                    "user": serializer.data,
                    "token": token.key  # Return the token
                }, status=status.HTTP_201_CREATED)


# from .serializers import UserLoginSerializer  # Ensure you have the serializer imported
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": "Logged in successfully",
                "user": {
                    "email": user.email,
                    "username": user.username,  # Return more user details
                    # Add other fields as necessary
                },
                "token": token.key
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)




class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        request.user.auth_token.delete()  # Delete the token
        logout(request)
        return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
