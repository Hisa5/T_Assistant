from django.urls import path
from .views import UserRegisterView, LoginView, LogoutView, ChangePasswordView, VerifyEmailView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
]
