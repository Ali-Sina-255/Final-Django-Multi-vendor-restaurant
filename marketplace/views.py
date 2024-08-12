from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from menu.models import Category, FootItem
from vendor.models import Vendor, OpeningHour
from marketplace.models import Cart
from orders.forms import OrderForms
from .context_processors import get_cart_counter, get_cart_amounts
from datetime import datetime, date, time


# Create your views here.
@login_required(login_url="login")
def marketplace_view(request):
    query = request.GET.get('rest_name', '').strip()  # Get the search input from the request and strip any leading/trailing whitespace
    
    print(f"Search Query: '{query}'")  # Debug: Check if the query is being captured correctly

    if query:
        # Debug: Check if the filtering returns any results
        vendors = Vendor.objects.filter(vendor_name__icontains=query, is_approved=True, user__is_active=True)
        print(f"Filtered Vendors: {vendors}")  # Debug: Print the filtered vendors to see if any match the query
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)

    vendor_count = vendors.count()
    
    # Debug: Check if the filtering returns any results
    print(f"Vendors found: {vendor_count}")
    
    context = {
        "vendors": vendors,
        "vendor_count": vendor_count,
        "query": query
    }
    return render(request, "marketplace/listing.html", context)
def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch("fooditems", queryset=FootItem.objects.filter(is_available=True))
    )
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by(
        "day", "-from_hour"
    )
    today_date = date.today()
    print(today_date)
    today = today_date.isoweekday()
    print(today)
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
    else:
        cart_item = 0

    context = {
        "vendor": vendor,
        "categories": categories,
        "cart_item": cart_item,
        "opening_hours": opening_hours,
        "current_opening_hours": current_opening_hours,
    }
    return render(request, "marketplace/vendor_detail.html", context)


def add_to_cart_view(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # check if the food item is exist in the cart
            try:
                food_item = FootItem.objects.get(id=food_id)
                print(food_item)
                # if the user is already added to the cart
                try:
                    check_cart = Cart.objects.get(
                        user=request.user, food_item=food_item
                    )
                    # increase the cart item
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "Increased the cart quantity",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                            "cart_amount": get_cart_amounts(request),
                        }
                    )

                except:
                    check_cart = Cart.objects.create(
                        user=request.user, food_item=food_item, quantity=1
                    )
                    return JsonResponse(
                        {
                            "status": "Success",
                            "message": "added to the card item",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                            "cart_amount": get_cart_amounts(request),
                        }
                    )

            except:
                return JsonResponse(
                    {"status": "Failed", "message": "this food does not exist!"}
                )

        else:

            return JsonResponse({"status": "Failed", "message": "Invalid Request"})

    return JsonResponse(
        {"status": "login_required", "message": "Please login to continue"}
    )


def decrease_cart_view(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # check if the food item is exist in the cart
            try:
                food_item = FootItem.objects.get(id=food_id)
                print(food_item)
                # if the user is already added to the cart
                try:
                    check_cart = Cart.objects.get(
                        user=request.user, food_item=food_item
                    )
                    # decrease the cart item
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse(
                        {
                            "status": "success",
                            "cart_counter": get_cart_counter(request),
                            "qty": check_cart.quantity,
                            "cart_amount": get_cart_amounts(request),
                        }
                    )

                except:
                    return JsonResponse(
                        {
                            "status": "Failed",
                            "message": "You don't have this item in your cart",
                        }
                    )

            except:
                return JsonResponse(
                    {"status": "Failed", "message": "this food does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid Request"})

    return JsonResponse(
        {"status": "login_required", "message": "Please login to continue"}
    )


def cart_view(request):
    cart_item = Cart.objects.filter(user=request.user).order_by("-created_at")
    context = {"cart_item": cart_item}
    return render(request, "marketplace/cart.html", context)


@login_required(login_url="login")
def delete_cart_view(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                cart = request.session.get('cart', {})
                if cart_item:
                    cart_item.delete()
                    return JsonResponse(
                        {
                            "status": "success",
                            "cart":cart,
                            "message": "cart item has been deleted",
                            "cart_counter": get_cart_counter(request),
                            "cart_amount": get_cart_amounts(request),
                        }
                    )
            except:
                return JsonResponse(
                    {"status": "Failed", "message": "this food does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid Request"})


def search_view(request):
    return HttpResponse("search")

def checkout_view(request):
    cart_item = Cart.objects.filter(user=request.user)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect("marketplace")

    user_profile = UserProfile.objects.get(user=request.user)
    default_value = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "phone_number": request.user.phone_number,
        "email": request.user.email,
        "address": user_profile.address,
        "state": user_profile.state,
        "city": user_profile.city,
    }
    form = OrderForms(initial=default_value)
    context = {"form": form, "cart_item": cart_item}
    return render(request, "marketplace/checkout.html", context)
