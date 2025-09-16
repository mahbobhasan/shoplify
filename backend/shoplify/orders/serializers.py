from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Order,OrderItem
from products.models import Product
from orders.models import CustomUser

from products.serializers import ProductSerializer
from accounts.serializers import UserProfileSerializer

class OrderItemSerilizer(ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"
class OrderSerializer(ModelSerializer):
    items=OrderItemSerilizer(read_only=True,many=True)
    class Meta:
        model=Order
        fields=["user","status","order_address","mobile","o_division","items"]
        extra_kwargs={
            "status":{"read_only":True}
        }


