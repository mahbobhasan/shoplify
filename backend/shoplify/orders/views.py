from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import   Order,Product,OrderSerializer,OrderItem
from Generalization.GeneralViews import Generalize
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_list_or_404
from rest_framework import status
# Create your views here.


class OrderListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    generalize=Generalize(OrderSerializer,Order)
    def post(self,request):
        return self.generalize.post_new_obj(request=request)
    def get(self,request):
        orders=get_list_or_404(Order,user=request.user)
        serilizer=OrderSerializer(orders,many=True,context={"context":request})
        return Response(data=serilizer.data,status=status.HTTP_200_OK)


