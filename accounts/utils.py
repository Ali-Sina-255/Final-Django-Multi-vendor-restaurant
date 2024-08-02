from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def detect_user(user):
    if user.role == 1:
        redirect_url = "vendor_dashboard"
        return redirect_url
    elif user.role == 2:
        redirect_url = "customer_dashboard"
        return redirect_url
    elif None == user.role and user.is_admin:
        redirect_url = "/admin"
        return redirect_url


def send_verification_email(request, user, email_subject, email_template):
    current_site = get_current_site(request)
    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email

    mail = EmailMessage(email_subject, message, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_reset_password_email(request, user):
    form_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    email_subject = "Reset your password "
    message = render_to_string(
        "account/email/reset_password_email.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(email_subject, message, form_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if isinstance(context["to_email"], str):
        to_email = []
        to_email.append(context["to_email"])
    else:
        to_email = context["to_email"]
    mail = EmailMessage(mail_subject, message, from_email, to_email)
    mail.content_subtype = "html"
    mail.send()
