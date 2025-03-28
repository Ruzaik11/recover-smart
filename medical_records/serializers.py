from rest_framework import serializers
from checklists.serializers import ChecklistSerializer
from medical_records.models import MedicalRecord  # Import the MedicalRecord model

class MedicalRecordSerializer(serializers.ModelSerializer):

    checklists = ChecklistSerializer(many=True, read_only=True, source='checklist_set')  # Add related checklists
    patient_full_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'created_by', 'create_date', 'patient_full_name', 'symptoms', 'diagnosis', 'treatment', 'allergies', 'status','checklists']

    def get_patient_full_name(self, obj):
        # Concatenate first_name and last_name
        return f"{obj.patient.first_name} {obj.patient.last_name}"