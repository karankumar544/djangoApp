from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    get_user_table,
)
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_verification_email, verify_token_from_email
from django.contrib.auth import authenticate


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_verification_email(serializer.validated_data["email"])
            return Response(
                {"message": "Registered! Please verify your email."}, status=201
            )
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            # Since user is valid, create token manually using email
            # We'll create a mock user-like object with just the ID/email
            class SimpleUser:
                def __init__(self, email):
                    self.id = email  # JWT needs an 'id' field (USER_ID_FIELD)

            user = SimpleUser(email=email)

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Send password reset email
            return Response({"message": "Password reset link sent."})
        return Response(serializer.errors, status=400)


class VerifyEmailView(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        token = request.query_params.get("token")
        if verify_token_from_email(email, token):
            table = get_user_table()
            table.update_item(
                Key={"email": email},
                UpdateExpression="SET is_verified = :val1",
                ExpressionAttributeValues={":val1": True},
            )
            return Response({"message": "Email verified!"})
        return Response({"error": "Invalid token or email."}, status=400)
