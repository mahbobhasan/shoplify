from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import OrderItem,OrderHistory,CustomUser,Product,Order

class OrderItemSerializer(serializers.ModelSerializer):
    product=serializers.IntegerField(source="product.product_id",read_only=True)
    product_name=serializers.CharField(source="product.product_name",read_only=True)
    product_price=serializers.DecimalField(source="product.unit_price",read_only=True,max_digits=10,decimal_places=2)
    user=serializers.IntegerField(source="user.id",read_only=True)
    class Meta:
        model=OrderItem
        fields="__all__"
        read_only_fields = ["user"]
    def validate_product(self,value):
        if self.context['request'].method=="POST":
            print("hellos")
            prot=OrderItem.objects.filter(product=value,user=self.context['request'].user)
            print("This is prot", prot)
            if prot:
                raise ValidationError({"error":"This product is already in your cart."})
            print("validatin done")
            return value
        return value

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderHistory
        exclude=("created_at",)
        read_only_fields = ["user", "created_at"]
class OrderSerializer(serializers.ModelSerializer):
    order_histories=OrderHistorySerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields="__all__"
        read_only_fields = ["user", "created_at"]
