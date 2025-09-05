from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include("accounts.urls"), name="accounts"),
    path('products/',include("products.urls"),name="products"),
    path('orders/',include("orders.urls"),name="orders")
]
