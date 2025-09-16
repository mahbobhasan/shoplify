from django.db import models
from products.models import Product
from accounts.models import CustomUser
# Create your models here.

class OrderStatus(models.TextChoices):
    PENDING="pending","Pending"
    CONFIRMED="confirmed","Confirmed"
    CANCELLED="cancelled","Cancelled"
    FAILED="failed","Failed"
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=30,default=OrderStatus.PENDING)
    order_address = models.TextField()
    mobile = models.CharField(max_length=14,null=True)
    o_division = models.CharField(max_length=14,null=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        verbose_name="OrderItems"
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.product} in {self.order}"


class Transaction(models.Model):
    pass