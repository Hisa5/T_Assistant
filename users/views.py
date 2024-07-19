from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser as User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django_rest_passwordreset.views import ResetPasswordRequestToken

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()  # Esto permite acceso sin autenticación

    def perform_create(self, serializer):
        user = serializer.save()
        # Send verification email here if needed

class VerifyEmailView(views.APIView):
    # Implement email verification logic here
    pass

class LoginView(views.APIView):
    permission_classes = ()  # Esto permite acceso sin autenticación

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class ChangePasswordView(ResetPasswordRequestToken):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
