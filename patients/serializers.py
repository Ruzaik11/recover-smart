from .models import Patient
from rest_framework import serializers

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile','user_id']  # Include only relevant fields
