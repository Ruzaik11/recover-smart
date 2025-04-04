from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .serializers import DoctorSerializer
from rest_framework import status
from .models import Doctor
from django.db.models import Q
import logging

logger = logging.getLogger("myapp")

# Create your views here.
class DoctorsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]  # ✅ Ensure it accepts JSON requests

    def get(self, request):
        if not request.user.has_perm("doctor.view_doctor"):
            return Response(
                {"error": "You do not have permission to view this doctor record"},
                status=403,
            )

        search = request.GET.get("search", "")
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        ).order_by('-id')
        serializer = DoctorSerializer(
            doctors, many=True, context={"include_items": False}
        )
        return Response(serializer.data)

    @api_view(["GET"])
    def edit(request, pk):
        # Check permission
        if not request.user.has_perm("doctor.view_doctor"):
            return Response(
                {"error": "You do not have permission to view this doctor record"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            # Fetch the doctor
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the doctor
        doctor_data = DoctorSerializer(doctor).data

        return Response(doctor_data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.has_perm("doctor.add_doctor"):
            return Response(
                {"error": "You do not have permission to add a doctor record"},
                status=403,
            )
        
        data = request.data.copy()
        serializer = DoctorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        if not request.user.has_perm("doctor.change_doctor"):
            return Response(
                {"error": "You do not have permission to change this doctor record"},
                status=403,
            )
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if not request.user.has_perm("doctor.delete_doctor"):
            return Response(
                {"error": "You do not have permission to delete a doctor record"},
                status=403,
            )
        try:
            doctor = Doctor.objects.get(pk=pk)
            doctor.delete()
            return Response({}, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
