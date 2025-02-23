from rest_framework import serializers
from .models import ChecklistItem  # Import the MedicalRecord model

class ChecklistItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChecklistItem
        fields = ['id', 'checklist', 'type', 'title', 'description', 'due_date', 'task_status', 'complete_date']
