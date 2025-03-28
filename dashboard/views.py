from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from medical_records.serializers import MedicalRecordSerializer
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer
from rest_framework import status
from patients.models import Patient
from doctors.models import Doctor
from checklist_items.models import ChecklistItem
from checklist_items.serializers import ChecklistItemSerializer
import pprint
from django.db.models import Q
import sys
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger("myapp")
# Create your views here.
class DashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]   # ✅ Ensure it accepts JSON requests

    def get(self, request):
        # Number of Patients
        # Doctors
        # Recovery Completion Rate
        # Average Recovery Time

        patients = PatientSerializer(Patient.objects.filter(), many=True).data
        totalPatients = len(patients)
        doctors = DoctorSerializer(Doctor.objects.filter(), many=True).data
        totalDoctors = len(doctors)

        checklistitem = ChecklistItem.objects.filter()
        listItem = ChecklistItemSerializer(checklistitem, many=True).data
        totalCheckListItems = len(listItem)
        completedCheckListItems = len([item for item in listItem if item['task_status'] == 1])
        recoveryCompletionRate = (completedCheckListItems / totalCheckListItems) * 100 if totalCheckListItems > 0 else 0

        totalRecoveryTime = 0
        validItems = 0
        for item in listItem:
            if item['task_status'] == 1:
                complete_date = item.get('complete_date')
                due_date = item.get('due_date')
                if complete_date and due_date:
                    try:
                        # Ensure both dates are parsed as datetime objects
                        complete_date = datetime.strptime(complete_date, "%Y-%m-%d")
                        due_date = datetime.strptime(due_date, "%Y-%m-%d")
                        totalRecoveryTime += (complete_date - due_date).days
                        validItems += 1
                    except Exception as e:
                        logger.error(f"Error calculating recovery time for item {item}: {e}")

        averageRecoveryTime = totalRecoveryTime / validItems if validItems > 0 else 0

        # Log the values for debugging
        logger.debug(f"Total Patients: {totalPatients}")
        logger.debug(f"Total Doctors: {totalDoctors}")
        logger.debug(f"Recovery Completion Rate: {recoveryCompletionRate}")
        logger.debug(f"Average Recovery Time: {averageRecoveryTime}")

        return Response({
            'totalPatients': totalPatients,
            'totalDoctors': totalDoctors,
            'recoveryCompletionRate': recoveryCompletionRate,
            'recoveryTime': averageRecoveryTime,
        }, status=status.HTTP_200_OK)


