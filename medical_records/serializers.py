from rest_framework import serializers
from checklists.serializers import ChecklistSerializer
from medical_records.models import MedicalRecord  # Import the MedicalRecord model

class MedicalRecordSerializer(serializers.ModelSerializer):

    checklists = ChecklistSerializer(many=True, read_only=True, source='checklist_set')  # Add related checklists
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'created_by', 'create_date', 'symptoms', 'diagnosis', 'treatment', 'allergies', 'status','checklists']

    