from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product,Category
class ProductSerializer(ModelSerializer):
    image_url=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields = [
            "product_id",
            "category",
            "product_name",
            "unit_price",
            "quantity",
            "cost_price",  # Write-only field
            "image",
            "image_url"
        ]
        extra_kwargs={
            "cost_price":{"write_only":True},
            "image":{"write_only":True}
        }
    def get_image_url(self,obj):
        request=self.context['request']
        if obj.image and request:
            print(obj.image.url)
            return request.build_absolute_uri(obj.image.url)
        else:
            return None
    
    def validate(self, attrs):
        """Validate quantity, cost price, and unit price based on request type."""
        request_method = self.context['request'].method  # GET, POST, PUT, PATCH, DELETE

        # Extract fields if provided in request
        quantity = attrs.get("quantity")
        cost_price = attrs.get("cost_price")
        unit_price = attrs.get("unit_price")

        # 🔹 For POST request → require all fields
        if request_method == "POST":
            if quantity is None or cost_price is None or unit_price is None:
                raise serializers.ValidationError("Quantity, cost price, and unit price are required.")

        # 🔹 For both POST & PATCH → validate only provided fields
        if quantity is not None and quantity < 1:
            raise serializers.ValidationError("Quantity must be a positive integer.")

        if cost_price is not None and unit_price is not None:
            if cost_price > unit_price:
                raise serializers.ValidationError("Cost price cannot be greater than unit price.")

        return attrs

class CategorySerializer(ModelSerializer):
    products=ProductSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields=["category_name","products"]