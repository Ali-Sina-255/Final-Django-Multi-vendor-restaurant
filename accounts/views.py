from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages, auth

from .forms import UserRegistrationForm
from .models import User, UserProfile
from vendor.forms import VendorRegisterForm
from .utils import detect_user, send_reset_password_email, send_verification_email
from orders.models import Order
from vendor.models import Vendor
import datetime


# Restrict the vendor from accessing the customers page
def check_rol_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied


# Restrict the vendor from accessing the customers page
def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied


def user_registration(request):
    if request.user.is_authenticated:
        messages.warning(request, "your are already registered")
        return redirect("my_account")
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.role = User.CUSTOMER
            user.save()
            # send the verification email
            mail_subject = "Please Activate your Registration"
            email_template = "account/email/verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Your registration was successfully")
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "account/register.html", context)


def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "your are already registered")
        return redirect("my_account")
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        vendor_form = VendorRegisterForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor_name = vendor_form.cleaned_data["vendor_name"]
            vendor.vendor_slug = slugify(vendor_name) + "-" + str(user.pk)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send the verification email
            mail_subject = "Confirm  your account Registrations "
            email_template = "account/email/verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(
                request,
                "Your restaurant registration has been registered  successfully! please with for the "
                "approval.",
            )
            return redirect("register_vendor")
        else:
            messages.error(request, "Registration was not registered successfully")
            print(form.errors)
            print(vendor_form.errors)
            return redirect("register_vendor")

    else:
        form = UserRegistrationForm()
        vendor_form = VendorRegisterForm()
    context = {
        "form": form,
        "vendor_form": vendor_form,
    }
    return render(request, "account/register_restaurant.html", context)


def activate(request, uidb64, token):
    # activated the user by settings the is_active to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "congratulation your account is activated")
        return redirect("my_account")
    else:
        messages.error(request, "Invalid Activation links")
        return redirect("my_account")


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("my_account")
    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "you are logged in Now")
            return redirect("my_account")
        else:
            messages.error(request, "Invalid Credentials !")
            return redirect("login")
    return render(request, "account/login.html")


def logout_view(request):
    auth.logout(request)
    messages.error(request, "you are logged out now")
    return redirect("login")


def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)
            mail_subject = "Reset your password"
            email_template = "account/email/reset_password_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            send_reset_password_email(request, user)
            messages.success(
                request, "Your password reset link has been sent to your email address"
            )
            return redirect("login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgot_password")

    return render(request, "account/forgot_password.html")


def reset_password_validate_view(request, uidb64, token):
    # Validate the user by decoding the token and user primary key
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "please reset your password")
        return redirect("reset_password")
    else:
        messages.error(request, "this link has been expired")
        return redirect("my_account")


def reset_password_view(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.asave()
            messages.success(request, "your password has been reset successfully")
            return redirect("login")

        else:
            messages.error(request, "password dont match")
            return redirect("reset_password")
    return render(request, "account/reset_password.html")


@login_required(login_url="login")
def my_account_view(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def vendor_dashboard_view(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_order=True)
    recent_order = orders[:10]

    current_month = datetime.datetime.now().month
    current_month_order = orders.filter(
        vendors__in=[vendor.id], created_at__month=current_month
    )
    current_month_revenue = 0
    for i in current_month_order:
        current_month_revenue += i.get_total_by_vendor()

    total_revenue = 0

    for i in orders:
        total_revenue += i.get_total_by_vendor()

    context = {
        "orders": orders,
        "order_count": orders.count(),
        "recent_order": recent_order,
        "total_revenue": total_revenue,
        "current_month_revenue": current_month_revenue,
    }
    return render(request, "account/vendor_dashboard.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_customer)
def customer_dashboard_view(request):
    orders = Order.objects.filter(user=request.user, is_order=True)[:10]
    context = {"orders": orders, "order_count": orders.count()}
    return render(request, "account/customer_dashboard.html", context)
