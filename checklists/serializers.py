from rest_framework import serializers
from .models import Checklist
from checklist_items.serializers import ChecklistItemSerializer  # Import the ChecklistItemSerializer

class ChecklistSerializer(serializers.ModelSerializer):

    checklistItems = ChecklistItemSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Checklist
        fields = ['id', 'created_date', 'status', 'created_by','record', 'checklistItems']
