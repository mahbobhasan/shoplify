from django.urls import path 
from .views import UserRegisterAPIView,UserLoginAPIView,ChangePasswordAPIView,UserProfileAPIView,VerifyView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path('verify-otp/<int:id>/',VerifyView.as_view()),
   
]