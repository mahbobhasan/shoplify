from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Product
from .serializers import ProductSerializer , ProductListSerializer
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
            product=get_object_or_404(Product,pk=pk)
            product.delete()
            return Response({"message":"successfully deleted"},status=status.HTTP_200_OK)
        return Response(data={"error":"only admin can delete a  product"}, status=status.HTTP_403_FORBIDDEN)

class RelatedProductsView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        related_products = Product.objects.filter(category=product.category).exclude(product_id=product_id)

        serializer = ProductListSerializer(related_products, many=True, context={'request': request})
        return Response(serializer.data)
class ProductSearchView(APIView):
    """
    Search products by name and return related products in the same category.
    Example: /api/products/search/?q=phone
    """
    def get(self, request,search_key):
        
        if not search_key:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        
        matched_products = Product.objects.filter(product_name__icontains=search_key)

        if not matched_products.exists():
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

       
        categories = matched_products.values_list('category', flat=True).distinct()

        
        final_products = matched_products 

        serializer = ProductListSerializer(final_products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
