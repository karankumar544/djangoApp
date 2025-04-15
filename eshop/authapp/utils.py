# utils.py

import hashlib
from urllib.parse import urlencode
from django.conf import settings
from django.core.mail import send_mail


def generate_verification_token(email: str) -> str:
    """Generate SHA256 hash token using email."""
    return hashlib.sha256(email.encode()).hexdigest()


def send_verification_email(email: str) -> dict:
    """Send a verification email using Django's send_mail function."""

    if not email:
        return {"success": False, "status_code": 400, "message": "Email is required."}

    try:
        token = generate_verification_token(email)

        # Construct verification URL
        base_url = "http://localhost:8000"  # Replace with production domain
        query_string = urlencode({"email": email, "token": token})
        verification_link = f"{base_url}/api/auth/verify-email/?{query_string}"

        # Compose email
        subject = "Verify Your Email"
        message = (
            f"Hi,\n\nPlease verify your email by clicking the link below:\n"
            f"{verification_link}\n\nThanks!"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list)

        return {
            "success": True,
            "status_code": 200,
            "message": "Verification email sent successfully.",
        }

    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Failed to send email.",
            "details": str(e),
        }


def verify_token_from_email(email: str, token: str) -> bool:
    """Verify token sent in email link."""
    expected = generate_verification_token(email)
    return expected == token
