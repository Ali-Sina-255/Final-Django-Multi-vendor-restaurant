from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserInForm, UserProfileForm
from accounts.models import UserProfile, User
from django.contrib import messages
from orders.models import Order, OrderedFood


# Create your views here.
login_required(login_url="login")
def customer_profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "your profile is updated successfully")
            return redirect("c_profile")
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, "your profile is not updated")
            return redirect("c_profile")
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInForm(instance=request.user)
    context = {"profile_form": profile_form, "user_form": user_form, "profile": profile}
    return render(request, "customers/c_profile.html", context)


def my_orders_view(request):
    orders = Order.objects.filter(user=request.user, is_order=True).order_by(
        "-created_at"
    )
    context = {"orders": orders}
    return render(request, "customers/my_order.html", context)


def order_detail_view(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_order=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += item.price * item.quantity

        print(ordered_food)

        context = {"order": order, "ordered_food": ordered_food, "subtotal": subtotal}
        return render(request, "customers/order_details.html", context)
    except:
        return redirect("customer")
