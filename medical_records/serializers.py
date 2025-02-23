from rest_framework import serializers
from medical_records.models import MedicalRecord  # Import the MedicalRecord model

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'created_by', 'create_date', 'symptoms', 'diagnosis', 'treatment', 'allergies', 'status']