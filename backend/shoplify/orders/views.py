from rest_framework.views import APIView
from django.shortcuts import get_list_or_404,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, OrderHistory,Product,OrderStatus
from .serializers import OrderSerializer, OrderItemSerializer, OrderHistorySerializer
from Generalization.GeneralViews import Generalize


# ---------- Order Views ----------
class OrderListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        user=request.user
        items=get_list_or_404(OrderItem,user=user)

        if serializer.is_valid():
            order=serializer.save(user=request.user)
            print(serializer.data)  
            for item in items:
                qty=item.quantity
                orderhistory=OrderHistory.objects.create(order=order,user=user,product=item.product,quntity=qty)
                # print(orderhistory)
                item.product.quantity=item.product.quantity-qty
                item.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    generalize=Generalize(serializer=OrderSerializer,model=Order)
    def get(self, request, pk):
        return self.generalize.get_obj_details(request=request,pk=pk)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- OrderItem Views ----------
class OrderItemListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        items = OrderItem.objects.filter(user=request.user)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = OrderItemSerializer(data=request.data,context={"request":request})

        product=get_object_or_404(Product,pk=request.data["product"])
        if(product.quantity<int(request.data['quantity'])):
            return Response({"Error":f"We have shortage of this product. please select less than {product.quantity}"},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user=request.user,product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        print(request.data)
        data=request.data
        item=get_object_or_404(OrderItem,user=request.user,product=data['product'])
        serializer = OrderItemSerializer(item,data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,prd):
        item=get_object_or_404(OrderItem,user=request.user,product=prd)
        item.delete()
        return Response({"message":"Deleted"},status=status.HTTP_200_OK)



# ---------- OrderHistory Views ----------
class OrderHistoryListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        histories = OrderHistory.objects.filter(user=request.user)
        serializer = OrderHistorySerializer(histories, many=True)
        return Response(serializer.data)
