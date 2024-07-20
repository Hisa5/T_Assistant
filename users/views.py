from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .serializers import UserSerializer
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        self.send_verification_email(user)
        return Response({"message": "Registration successful. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"{self.request.scheme}://{self.request.get_host()}/api/users/verify-email/{uid}/{token}/"
        subject = "Verify your T-Assistant account"
        message = f"Dear {user.username},\n\nThank you for registering. Please click the link below to verify your email:\n{verification_link}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(views.APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        logger.debug(f"Attempting login for username: {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.email_verified:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                logger.debug(f"Login successful for username: {username}")
                return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                logger.debug(f"Email not verified for username: {username}")
                return Response({'error': 'Email not verified'}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(f"Invalid credentials for username: {username}")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class ChangePasswordView(ResetPasswordRequestToken):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class VerifyEmailView(views.APIView):
    permission_classes = []

    @method_decorator(csrf_exempt, name='dispatch')
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({"message": "Email successfully verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(ResetPasswordRequestToken):
    permission_classes = []

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(ResetPasswordConfirm):
    permission_classes = []
