from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Product,Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields=[""]