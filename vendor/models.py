from django.db import models
from django.forms import ValidationError
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_profile"
    )
    vendor_name = models.CharField(max_length=255)
    vendor_slug = models.SlugField(max_length=255)
    vendor_licenses = models.ImageField(upload_to="vendor/licenses")
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    update_om = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        print(today)
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start_time = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end_time = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start_time and current_time < end_time:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = "account/email/admin_approved.html"
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved,
                    "to_email": self.user.email,
                }
                if self.is_approved:
                    mail_subject = "Congratulations! Your restaurant has been approved"
                else:
                    mail_subject = "We're sorry, you are not eligible for publishing your food menu on our marketplace."

                # Send notification
                send_notification(mail_subject, mail_template, context)

        super(Vendor, self).save(*args, **kwargs)


DAY_CHOICES = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]
HOUR_OF_DAY_24 = [
    (time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p"))
    for h in range(0, 24)
    for m in range(0, 31, 30)
]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAY_CHOICES)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "-from_hour")
        unique_together = ("vendor", "day", "from_hour", "to_hour")

    def __str__(self) -> str:
        return self.get_day_display()


class ReviewRatting(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    review = models.TextField()
    ratting = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject
