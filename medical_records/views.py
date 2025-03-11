from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from medical_records.serializers import MedicalRecordSerializer
from patients.serializers import PatientSerializer
from rest_framework import status
from .models import MedicalRecord
from patients.models import Patient
import pprint
from django.db.models import Q
import sys
import logging

logger = logging.getLogger("myapp")
# Create your views here.
class MedicalRecordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    @api_view(['GET'])
    def getMyRecords(request):
        
        try:
            patient = Patient.objects.get(user_id=request.user.id)  # Find the patient for the current user
        except Patient.DoesNotExist:
            return Response({"error": "Patient matching query does not exist."}, status=HTTP_404_NOT_FOUND)
        
        patientSerializer = PatientSerializer(patient)
        medicalRecords = MedicalRecord.objects.filter(patient_id=patient.id)  # Use patient.id for filtering
        serializer = MedicalRecordSerializer(medicalRecords, many=True)
        
        return Response(serializer.data)
    
    def get(self, request, pk):
        if not request.user.has_perm("medical_record.view_medicalrecord"):
           return Response({"error": "You do not have permission to view this medical record"}, status=403)
        search = request.GET.get('search', '')
        patients = MedicalRecord.objects.filter(patient_id=pk)
        serializer = MedicalRecordSerializer(patients, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        if not request.user.has_perm("medical_record.add_medicalrecord"):
            return Response({"error": "You do not have permission to add a medical record"}, status=403)
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        if not request.user.has_perm("medical_record.change_medicalrecord"):
            return Response({"error": "You do not have permission to change this medical record"}, status=403)
        try:
            medicalrecord = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "medical record not found"}, status=404)
        serializer = MedicalRecordSerializer(medicalrecord, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
