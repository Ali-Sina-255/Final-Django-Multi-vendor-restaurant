from .models import Cart
from menu.models import FootItem


def get_cart_counter(request):
    cart_count = 0
    tax = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal_af = 0
    grand_total_usd = 0
    afghani_to_dollar_rate = 72  # 1 dollar = 72 afghani

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            food_item = FootItem.objects.get(pk=item.food_item.id)
            subtotal_af += food_item.price * item.quantity
        
        grand_total_usd = round(subtotal_af / afghani_to_dollar_rate, 2)

    return dict(
        subtotal_af=subtotal_af,
        grand_total_usd=grand_total_usd
    )


