from django.urls import path
from .views import ProductListCreateAPIView,ProductDetailAPIView , RelatedProductsView , ProductSearchView
urlpatterns=[
    path("",ProductListCreateAPIView.as_view(),name="product-list-create"),
    path("<int:pk>/",ProductDetailAPIView.as_view(),name="product-details"),
    path('related/<int:product_id>/', RelatedProductsView.as_view(), name='related-products'),
    path('search/' , ProductSearchView.as_view(), name='product-search')
]