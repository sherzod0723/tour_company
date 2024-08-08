from django.db import models
from tour.models import Tour
from user.models import User


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=255, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="orderitem")
    count = models.IntegerField()
    total = models.DecimalField(max_digits=255, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tour.country)

