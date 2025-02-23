
from doctors.models import Doctor
from rest_framework import serializers

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name']

