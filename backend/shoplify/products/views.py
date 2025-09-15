from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#Import Custom Classes
from Generalization.GeneralViews import Generalize
# Create your views here.
        
class ProductListCreateAPIView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]    
    generalize=Generalize(ProductSerializer,Product)
    def get(self,request):
        return self.generalize.get_all_obj(request=request)
    def post(self,request):
        if request.user.is_staff:
            return self.generalize.post_new_obj(request=request)
        return Response(data={"error":"only admin can create a new product"}, status=status.HTTP_403_FORBIDDEN)

class ProductDetailAPIView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    generalize=Generalize(ProductSerializer,Product)
    def get(self,request,pk):
        return self.generalize.get_obj_details(request=request,pk=pk)
    def put(self,request,pk):
        if request.user.is_staff:
            return self.generalize.update_obj(request=request,pk=pk)
        return Response(data={"error":"only admin can create a new product"}, status=status.HTTP_403_FORBIDDEN)
    def patch(self,request,pk):
        if request.user.is_staff:
            return self.generalize.update_obj(request=request,pk=pk)
        return Response(data={"error":"only admin can update a  product"}, status=status.HTTP_403_FORBIDDEN)
    def delete(self,request,pk):
        if request.user.is_staff:
            return self.generalize.delete_obj(request=request,pk=pk)
        return Response(data={"error":"only admin can delete a  product"}, status=status.HTTP_403_FORBIDDEN)
    
class CategoryListCreateAPIView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    generalize=Generalize(CategorySerializer,model=Category)
    def post(self,request):
        if request.user.is_staff:
            return self.generalize.post_new_obj(request=request)
        return Response({"error":"only admin can create a new category"})
    def get(self,request):
        return self.generalize.get_all_obj(request=request)

class CategoryRetriveUpdateDeleteAPIView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    generalize=Generalize(serializer=CategorySerializer,model=Category)
    def get(self,request,pk):
        return self.generalize.get_obj_details(request=request,pk=pk)
    def put(self,request,pk):
        if request.user.is_staff:
            return self.generalize.update_obj(request=request,pk=pk)
        return Response(data={"error":"only admin can update a  product"}, status=status.HTTP_403_FORBIDDEN)