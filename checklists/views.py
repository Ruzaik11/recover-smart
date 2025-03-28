from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import ChecklistSerializer
from rest_framework import status
from .models import Checklist
import pprint
from django.db.models import Q
import sys
# Create your views here.
class Checklists(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    def get(self,request):
        checklist = Checklist.objects.all().select_related('record')
        serializer = ChecklistSerializer(checklist, many=True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def getChecklistByRecordId(request, pk):
        checklist = Checklist.objects.get(pk=pk)
        serializer = ChecklistSerializer(checklist)
        return Response(serializer.data)

    def post(self,request):
        try:
            serializer = ChecklistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Checklist.DoesNotExist:
            return Response({"error": "Checklist not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        try:
            checklist = Checklist.objects.get(pk=pk)
            serializer = ChecklistSerializer(checklist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Checklist.DoesNotExist:
            return Response({"error": "Checklist not found"}, status=status.HTTP_404_NOT_FOUND)