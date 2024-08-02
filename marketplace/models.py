from django.db import models
from accounts.models import User
from menu.models import FootItem


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(
        FootItem, on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user


class Tax(models.Model):
    tax_type = models.CharField(max_length=255)
    tax_percentage = models.DecimalField(
        decimal_places=2, max_digits=4, verbose_name="Tax percentage(%)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Tax"

    def __str__(self) -> str:
        return self.tax_type
