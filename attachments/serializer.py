from rest_framework import serializers
from .models import Attachment  # Import the MedicalRecord model

class attachment(serializers.ModelSerializer):
    
    class Meta:
        model = Attachment
        fields = ['id', 'entity', 'record_id', 'url']
