from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import ChecklistItemSerializer
from rest_framework import status
from .models import ChecklistItem
import pprint
from django.db.models import Q
import sys
# Create your views here.
class ChecklistsItem(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    def get(self,request,pk):
        checklistitem = ChecklistItem.objects.filter(checklist_id=pk)
        serializer = ChecklistItemSerializer(checklistitem, many=True)
        return Response(serializer.data)

    def post(self,request):
        try:
            serializer = ChecklistItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ChecklistItem.DoesNotExist:
            return Response({"error": "ChecklistItem Item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        try:
            checklistitem = ChecklistItem.objects.get(pk=pk)
            serializer = ChecklistItemSerializer(checklistitem, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ChecklistItem.DoesNotExist:
            return Response({"error": "ChecklistItem Item not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self,request,pk):
        try:
            checklistitem = ChecklistItem.objects.get(pk=pk)
            checklistitem.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChecklistItem.DoesNotExist:
            return Response({"error": "ChecklistItem Item not found"}, status=status.HTTP_404_NOT_FOUND)