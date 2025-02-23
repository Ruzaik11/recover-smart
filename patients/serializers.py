from rest_framework import serializers
from patients.models import Patient
from medical_records.serializers import MedicalRecordSerializer  # Import the MedicalRecordSerializer

class PatientSerializer(serializers.ModelSerializer):
    medical_records = MedicalRecordSerializer(many=True, read_only=True)  # Nested serializer
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'mobile', 'user', 'medical_records']

    def __init__(self, instance=None, **kwargs):
        include_items = kwargs.pop('context', {}).get('include_items', True)
        super().__init__(instance, **kwargs)
        if not include_items:
            self.fields.pop('medical_records')