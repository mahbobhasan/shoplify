from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_list_or_404,get_object_or_404

class Generalize:
    def __init__(self,serializer,model):
        self.serializer=serializer
        self.model=model
    def get_all_obj(self,request):
        objects=get_list_or_404(self.model)
        serilizer=self.serializer(objects,many=True,context={"request":request})
        return Response(serilizer.data,status=status.HTTP_200_OK)
    def post_new_obj(self,request):
        serializer=self.serializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message":"successfully created"},status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get_obj_details(self,request,pk):
        object=get_object_or_404(self.model,pk=pk)
        serializer=self.serializer(object,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update_obj(self,request,pk):
        object=get_object_or_404(self.model,pk=pk)
        serializer=self.serializer(object,data=request.data,partial=True,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"successfully updated"},status=status.HTTP_200_OK)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    def delete_obj(self,request,pk):
        object=get_object_or_404(self.model,pk=pk)
        object.delete()
        return Response({"message":"deleted successfully"},status=status.HTTP_200_OK)