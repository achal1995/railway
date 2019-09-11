import time
from .tokens import token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# from useraccounts.models import Users
from django.contrib.auth import get_user_model
Users = get_user_model()

from .models import ActivationToken, PasswordResetToken

# To send activation link
def activation_email(request, email, user):
    current_site = get_current_site(request)
    mail_subject = 'Verify your email address.'
    activation_token = token()
    # expiry of activation key is 1 day
    expiry_at = round(time.time() + (24 * 60 * 60))
    message = render_to_string('acc_active_email.html', {
        'domain': current_site.domain,
        'uid':Users.objects.get(email=email).id,
        'token':activation_token,
    })
    ActivationToken.objects.update_or_create(owner=user,defaults={'activation_token': activation_token, 'expiry_at': expiry_at})
    to_email = email
    # to_email = 'pathak.achal5@gmail.com'
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()

# To send password reset link
def password_reset_email(request, email, user):
    current_site = get_current_site(request)
    mail_subject = 'Password Reset.'
    reset_token = token()
    # expiry of reset token is 30mins
    expiry_at = round(time.time() + (30 * 60))
    message = render_to_string('pass_reset_email.html', {
        'domain': current_site.domain,
        'uid':Users.objects.get(email=email).id,
        'token':reset_token,
    })
    PasswordResetToken.objects.update_or_create(owner=user,defaults={'reset_token': reset_token, 'expiry_at': expiry_at})
    to_email = email
    # to_email = 'pathak.achal5@gmail.com'
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()