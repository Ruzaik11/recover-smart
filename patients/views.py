from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import PatientSerializer
from users.serializers import UserSerializer
from rest_framework import status
from .models import Patient
import pprint
from users.services import create_user_and_send_email
from django.db.models import Q
import sys
import logging

logger = logging.getLogger("myapp")
# Create your views here.
class Patients(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]  # ✅ Ensure it accepts JSON requests

    def get(self, request):

        if not request.user.has_perm("patients.view_patient"):
            return Response(
                {"error": "You do not have permission to view this patient record"},
                status=403,
            )

        search = request.GET.get("search", "")
        patients = Patient.objects.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)  # Fixed typo here
        ).order_by('-id')
        serializer = PatientSerializer(
            patients, many=True, context={"include_items": False}
        )
        return Response(serializer.data)

    @api_view(["GET"])
    def edit(request, pk):
        # Check permission
        if not request.user.has_perm("patients.view_patient"):
            return Response(
                {"error": "You do not have permission to view this patient record"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            # Fetch the patient and prefetch related medical records
            patient = Patient.objects.prefetch_related("medical_records").get(pk=pk)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the patient and their medical records
        patient_data = PatientSerializer(patient).data

        # Combine the data into a single response

        return Response(patient_data, status=status.HTTP_200_OK)

    def post(self, request):

        if not request.user.has_perm("patients.add_patient"):
            return Response(
                {"error": "You do not have permission to add a patient record"},
                status=403,
            )

        userData = {
            "username": request.data["username"],
            "email": request.data["email"],
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
        }

        data = request.data.copy()
        userSerializer = UserSerializer(data=userData)
        if userSerializer.is_valid():
            user = userSerializer.save()
            data["user"] = user.id
        else:
            return Response(user.errors, status=400)

        serializer = PatientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            create_user_and_send_email(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        if not request.user.has_perm("patients.change_patient"):
            return Response(
                {"error": "You do not have permission to change this patient record"},
                status=403,
            )
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=404)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    @api_view(["GET"])
    def userPatient(request):
 
        try:
            user = request.user
            # Fetch the patient and prefetch related medical records

            patient = Patient.objects.prefetch_related("medical_records").get(user=user.id)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        # Serialize the patient and their medical records
        patient_data = PatientSerializer(patient).data

        # Combine the data into a single response

        return Response(patient_data, status=status.HTTP_200_OK)
    

    def delete(self, request, pk):
        if not request.user.has_perm("patients.delete_patient"):
            return Response(
                {"error": "You do not have permission to delete a patient record"},
                status=403,
            )
        try:
            patient = Patient.objects.get(pk=pk)
            patient.delete()
            return Response({},status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error":'Patient not found'}, status = status.HTTP_404_NOT_FOUND)