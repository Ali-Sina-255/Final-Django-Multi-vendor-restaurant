import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amounts
from accounts.utils import send_notification
from menu.models import FootItem
from .forms import OrderForms
from .models import Order, Payment, OrderedFood
from .utils import generate_order_num, order_total_by_vendor
import logging


# Create your views here.


@login_required(login_url="login")
def order_place_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by("-created_at")
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect("marketplace")

    vendors_ids = []
    total_data = {}
    get_tax = Tax.objects.filter(is_active=True)
    for item in cart_items:
        if item.food_item.vendor.id not in vendors_ids:
            vendors_ids.append(item.food_item.vendor.id)

    subtotal = 0
    vendor_k = {}
    for i in cart_items:
        food_item = FootItem.objects.get(pk=i.food_item.id, vendor__id__in=vendors_ids)

        v_id = food_item.vendor.id
        if v_id in vendor_k:
            subtotal = vendor_k[v_id]
            subtotal += food_item.price * i.quantity
            vendor_k[v_id] = subtotal
        else:
            subtotal = food_item.price * i.quantity
            vendor_k[v_id] = subtotal

        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

        total_data.update({food_item.vendor.id: {str(subtotal): str(tax_dict)}})
    print(total_data)

    subtotal = get_cart_amounts(request)["grand_total_usd"]
    grand_total = get_cart_amounts(request)["grand_total_usd"]

    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            order = Order(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone_number=form.cleaned_data["phone_number"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
                state=form.cleaned_data["state"],
                city=form.cleaned_data["city"],
                user=request.user,
                total=grand_total,
                total_data=json.dumps(total_data),
                payment_method=request.POST["payment_method"],
            )
            order.save()
            order.order_number = generate_order_num(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            messages.success(request, "Your order was sent successfully!")

            context = {"order": order, "cart_items": cart_items}
            return render(request, "order/order_place.html", context)
        else:
            print(form.errors)
            messages.error(request, "Your order was not sent successfully!")
    else:
        # If it's a GET request, prepopulate with user's last order if it exists
        last_order = Order.objects.filter(user=request.user).last()
        if last_order:
            form = OrderForms(instance=last_order)
        else:
            form = OrderForms()

    context = {
        "form": form,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "grand_total": grand_total,
    }
    return render(request, "order/order_place.html", context)


@login_required(login_url="login")
def payments(request):
    # if the request is ajax or not
    if (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and request.method == "POST"
    ):
        order_number = request.POST.get("order_number")
        transaction_id = request.POST.get("transaction_id")
        payment_method = request.POST.get("payment_method")
        status = request.POST.get("status")

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status,
        )
        payment.save()
        order.payment = payment
        order.is_order = True
        order.save()

        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.food_item = item.food_item
            ordered_food.quantity = item.quantity
            ordered_food.price = item.food_item.price
            ordered_food.amount = item.food_item.price * item.quantity
            ordered_food.save()
            
        mail_subject = "Thank your for ordering with US."
        mail_template = "order/email/order_confirmation_email.html"
        order_food = OrderedFood.objects.filter(order=order)
        customer_subtotal = 0
        for total in order_food:
            customer_subtotal += (total.price * total.quantity )
        context = {
            "user": request.user, 
            "order": order, 
            "to_email": order.email,
            "order_food":order_food,
            "domain":get_current_site(request),
            "customer_subtotal": customer_subtotal
            
            }
        # send notification email to customer
        send_notification(mail_subject, mail_template, context)

        #   SEND NOTIFICATION EMAIL TO VENDOR

        mail_subject = "You have received new order"
        mail_template = "order/email/order_received_email.html"

        to_email = []
        for i in cart_items:
            if i.food_item.vendor.user.email is not to_email:
                to_email.append(i.food_item.vendor.user.email)
                order_food_to_vendor = OrderedFood.objects.filter(order=order, food_item__vendor=i.food_item.vendor)
                print(order_food_to_vendor)
       

                context = {
                    "order": order,
                    "to_email": i.food_item .vendor.user.email,
                    "order_food_to_vendor":order_food_to_vendor,
                    "vendor_subtotal":order_total_by_vendor(order,i.food_item.vendor.id) ['grand_total']
                }
                send_notification(mail_subject, mail_template, context)
    # cart_items.delete()
    response = {"order_number": order_number, "transaction_id": transaction_id}
    return JsonResponse(response)
    # update the order

    # store the payment detail in the payment model
    # update the order model
    # movie the cart item to order food model


def order_complete_view(request):
    order_number = request.GET.get("order_no")
    transaction_id = request.GET.get("trans_id")
    print(order_number)
    print(transaction_id)
    try:
        order = Order.objects.get(
            order_number=order_number,
            payment__transaction_id=transaction_id,
            is_order=True,
        )
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += item.price * item.quantity
        context = {"order": order, "ordered_food": ordered_food, "subtotal": subtotal}
        return render(request, "order/order_complete.html", context)
    except:
        return redirect("home")


def my_order_view(request):
    return render(request, "vendor/my_order.html")
