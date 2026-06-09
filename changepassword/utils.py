import secrets
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings


def generate_otp():
    return str(secrets.randbelow(1000000)).zfill(6)

def send_otp_email(email):
    otp=generate_otp()
    cache.set(f"otp_{email}", otp, timeout=300)
    cache.set(f"otp_attempts_{email}", 0, timeout=300)

    send_mail(
        subject="your otp verification code",
        message=f"your otp is {otp}\n\nvalid for 5 minutes only",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False

    )

def verify_otp(email, user_otp):
    stored_otp = cache.get(f"otp_{email}")
    attempts = cache.get(f"otp_attempts_{email}", 0)

    # OTP expired
    if stored_otp is None:
        return "expired"

    # Too many attempts
    if attempts >= 3:
        cache.delete(f"otp_{email}")
        return "blocked"

    # Wrong OTP
    if stored_otp != user_otp:
        cache.set(f"otp_attempts_{email}", attempts + 1, timeout=300)
        return "invalid"

    # Success — cleanup
    cache.delete(f"otp_{email}")
    cache.delete(f"otp_attempts_{email}")
    return "success"