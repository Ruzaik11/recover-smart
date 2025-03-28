from rest_framework import serializers
from .models import Checklist
from checklist_items.serializers import ChecklistItemSerializer  # Import the ChecklistItemSerializer

class ChecklistSerializer(serializers.ModelSerializer):
    checklistItems = ChecklistItemSerializer(many=True, read_only=True)  # Nested serializer
    diagnosis = serializers.CharField(source='record.diagnosis', read_only=True)
    patient_full_name = serializers.SerializerMethodField()
    total_checklist_items = serializers.SerializerMethodField()  # Use SerializerMethodField for dynamic calculation
    total_checklist_items_completed = serializers.SerializerMethodField()  # Use SerializerMethodField for dynamic calculation

    class Meta:
        model = Checklist
        fields = ['id', 'created_date', 'status', 'created_by', 'record', 'patient_full_name', 'diagnosis', 'checklistItems', 'total_checklist_items', 'total_checklist_items_completed']

    def get_patient_full_name(self, obj):
        # Concatenate first_name and last_name
        return f"{obj.record.patient.first_name} {obj.record.patient.last_name}"

    def get_total_checklist_items(self, obj):
        # Return the total count of checklist items
        return obj.checklistItems.count()

    def get_total_checklist_items_completed(self, obj):
        # Return the count of completed checklist items (assuming a 'status' field or similar)
        return obj.checklistItems.filter(task_status=1).count()