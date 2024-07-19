from django.conf import settings
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    uid = urlsafe_base64_encode(force_bytes(reset_password_token.user.pk))
    reset_url = f"{settings.FRONTEND_URL}/password_reset/confirm/?uid={uid}&token={reset_password_token.key}"
    
    email_plaintext_message = f"Please use the following link to reset your password: {reset_url}"

    send_mail(
        # title:
        "Password Reset for {title}".format(title="T-Assistant"),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email]
    )
