from django.urls import path
from .views import (
    OrderListCreateAPIView, OrderDetailAPIView,
    OrderItemListCreateAPIView,
    OrderHistoryListCreateAPIView,
)

urlpatterns = [
    path("", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("order-items/", OrderItemListCreateAPIView.as_view(), name="order-items"),
    path("order-items/<int:prd>", OrderItemListCreateAPIView.as_view(), name="order-items"),
    path("order-history/", OrderHistoryListCreateAPIView.as_view(), name="order-history"),
]
