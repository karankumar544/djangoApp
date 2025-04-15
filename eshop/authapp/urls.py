from django.urls import path
from .views import SignupView, LoginView, ForgotPasswordView, VerifyEmailView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
