from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Order,Cart
from products.models import Product
from orders.models import CustomUser

from products.serializers import ProductSerializer
from accounts.serializers import UserProfileSerializer


class CartSerializer(ModelSerializer):
    