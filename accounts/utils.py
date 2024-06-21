from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_verification_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    link = 'http://localhost:8000/api/verify-email/'+ uid+'/'+token+'/'
    emailw = EmailMessage(
        'Verify your email',
        'Click following link to verify your email:\n\n'+ link,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    emailw.send(fail_silently=False)
    return True

