from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import PatientSerializer
from medical_records.serializers import MedicalRecordSerializer
from rest_framework import status
from .models import Patient
import pprint
from django.db.models import Q
import sys

# Create your views here.
class Patients(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests
    
    def get(self, request):

        if not request.user.has_perm("patients.view_patient"):
            return Response({"error": "You do not have permission to view this patient record"}, status=403)

        search = request.GET.get('search', '')
        patients = Patient.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)  # Fixed typo here
        )
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    
    @api_view(['GET'])
    def edit(request, pk):
        # Check permission
        if not request.user.has_perm("patients.view_patient"):
            return Response({"error": "You do not have permission to view this patient record"}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the patient and prefetch related medical records
            patient = Patient.objects.prefetch_related('medical_records').get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the patient and their medical records
        patient_data = PatientSerializer(patient).data
        medical_records_data = MedicalRecordSerializer(patient.medical_records.all(), many=True).data

        # Combine the data into a single response
        response_data = {
            "patient": patient_data,
            "medical_records": medical_records_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):

        if not request.user.has_perm("patients.add_patient"):
            return Response({"error": "You do not have permission to add a patient record"}, status=403)

        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        if not request.user.has_perm("patients.change_patient"):
            return Response({"error": "You do not have permission to change this patient record"}, status=403)
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
