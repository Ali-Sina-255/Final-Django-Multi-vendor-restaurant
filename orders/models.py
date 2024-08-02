import json
from django.db import models
from accounts.models import User
from menu.models import FootItem
from vendor.models import Vendor
from decimal import Decimal


request_object = ""

PAYMENT_METHOD = (("Paypal", "PayPal"),)


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Complete", "Complete"),
        ("Accepted", "Accepted"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, null=True, blank=True
    )
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    total = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS, max_length=30, default="New")
    is_order = models.BooleanField(default="False")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def order_place_to(self):
        return ",".join([str(i) for i in self.vendors.all()])

    def get_total_by_vendor(self):
        try:
            # Get the current vendor from the request object
            vendor = Vendor.objects.get(user=request_object.user)
            subtotal = 0
            tax = 0
            tax_dict = {}

            if self.total_data:
                print(f"Total data before loading JSON: {self.total_data}")

                # Correctly load the total_data JSON
                total_data = json.loads(
                    self.total_data.replace("Decimal('", "").replace("')", "")
                )

                for vendor_id, vendor_data in total_data.items():
                    for price, tax_data in vendor_data.items():
                        subtotal += float(price)
                        tax_data = tax_data.replace("'", '"')
                        tax_data = json.loads(tax_data)
                        tax_dict.update(tax_data)

                        # Calculate tax
                        for currency, tax_info in tax_data.items():
                            for tax_rate, tax_amount in tax_info.items():
                                tax += float(tax_amount)

                grand_total = float(subtotal) + float(tax)

                # print('grand_total ==========>', grand_total)
                # print('tax ===========>', tax)
                # print('tax_dict ==========>', tax_dict)
                # print('subtotal ===========>', subtotal)

                context = {
                    "grand_total": grand_total,
                    "tax": tax,
                    "tax_dict": tax_dict,
                    "subtotal": subtotal,
                }
                return context  # Return the grand total context

            return 0  # Return 0 if there's no data for any vendor
        except json.JSONDecodeError as e:
            print(
                f"JSONDecodeError: {e} for order id: {self.id}, total_data: {self.total_data}"
            )
            return 0
        except KeyError as e:
            print(f"KeyError: {e} for order id: {self.id}")
            return 0
        except Exception as e:
            print(f"Unexpected error: {e} for order id: {self.id}")
            return 0

    def __str__(self) -> str:
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FootItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_item.food_title
