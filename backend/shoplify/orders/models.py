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
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="orders")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="orders")
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    sttaus=models.CharField(default=OrderStatus.PENDING)
    def __str__(self):
        return f"{self.user}->{self.product}"
class Cart(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='carts')
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='carts')
    quantity=models.PositiveIntegerField()

    class Meta:
        unique_together=("user_id","product_id")

    def __str__(self):
        return f"{self.user_id}->{self.product_id}"
class Transaction(models.Model):
    pass