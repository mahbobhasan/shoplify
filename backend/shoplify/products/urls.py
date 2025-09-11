from django.urls import path
from .views import ProductListCreateAPIView,ProductDetailAPIView,CategoryListCreateAPIView
urlpatterns=[
    path("",ProductListCreateAPIView.as_view(),name="product-list-create"),
    path("<int:pk>/",ProductDetailAPIView.as_view(),name="product-details"),
    path("categories/",CategoryListCreateAPIView.as_view(),name="categoires")
]