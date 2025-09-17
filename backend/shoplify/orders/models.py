from django.db import models
from accounts.models import CustomUser
from products.models import Product

# Create your models here.

class OrderStatus(models.TextChoices):
    PENDING="pending","Pending"
    CONFIRMED="confirmed","Confirmed"
    FAILED="failed","Failed"
    CANCELLED="cancelled","Cancelled"
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="orders")
    order_address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    mobile=models.CharField(max_length=14)
    o_division=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user}->{self.order_id}"


class OrderItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="items")
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together=("user","product")

class OrderHistory(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_histories")
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="order_histiories")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_histories")
    status=models.CharField(max_length=50,default=OrderStatus.PENDING)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    quntity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user}->{self.product}"
    class Meta:
        unique_together=("order","user","product")
