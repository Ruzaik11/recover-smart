from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_records")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    allergies = models.TextField()
    status = models.IntegerField()
    class Meta:
        db_table = "medical_records"
    

    def __str__(self):
        return f"Record {self.id} for {self.patient}"