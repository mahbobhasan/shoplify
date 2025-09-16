from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Product
from .serializers import ProductSerializer , ProductListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class ProductListCreateAPIView(APIView):
    # permission_classes=[IsAuthenticatedOrReadOnly]    
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True,context={"request":request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        if request.user.is_staff:
            serializer=ProductSerializer(data=request.data,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message":"successfully created"},status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error":"only admin can create a new product"}, status=status.HTTP_403_FORBIDDEN)

class ProductDetailAPIView(APIView):
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(product,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        if request.user.is_staff:
            product=get_object_or_404(Product,pk=pk)
            serializer=ProductSerializer(product,data=request.data,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"successfully updated"},status=status.HTTP_200_OK)
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error":"only admin can create a new product"}, status=status.HTTP_403_FORBIDDEN)
    def patch(self,request,pk):
        if request.user.is_staff:
            product=get_object_or_404(Product,pk=pk)
            serializer=ProductSerializer(product,data=request.data,partial=True,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"updated successfully"},status=status.HTTP_200_OK)
            return 
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
    def get(self, request):
        query = request.GET.get('q', '')  
        if not query:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        
        matched_products = Product.objects.filter(product_name__icontains=query)

        if not matched_products.exists():
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

       
        categories = matched_products.values_list('category', flat=True).distinct()
        related_products = Product.objects.filter(category__in=categories).exclude(id__in=matched_products.values_list('id', flat=True))

        
        final_products = matched_products | related_products

        serializer = ProductListSerializer(final_products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
