from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
import json
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import UserRegisterSerializer,UserLoginSerializer,ChangePasswordSerializer,UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random
from .models import CustomUser
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        print(request.data)
        token = random.randint(1000, 9999)
        if serializer.is_valid():
            user=serializer.save()
            user.token=token
            user.save()
            
            current_site = get_current_site(request)
            uid = user.id
            mail_subject = 'Activate your account'
            message = {
                'user': user.username,
                'domain': current_site.domain,
                'uid': uid,
                'token': token
            }
            email = EmailMessage(mail_subject, json.dumps(message), to=[user.email])
            print(message)
            email.send()
            return Response({"user":uid}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Only logged-in users can access

    def get(self, request):
        serializer = UserProfileSerializer(request.user)  # ✅ Serialize the logged-in user's data
        return Response(serializer.data, status=200)
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]  # User must be logged in

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyView(APIView):
    def put(self,request,id):
        data=request.data
        user=CustomUser.objects.get(pk=id)
        print(type(data['otp']),type(user.token),user.token)
        if int( data['otp'])==user.token:
            user.is_varified=True
            return Response({"success":"otp verified"}, status=status.HTTP_200_OK)
        return Response({"error":"wrong otp"}, status=status.HTTP_400_BAD_REQUEST)