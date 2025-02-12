from django.db import models
from patients.models import Patient

class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    class Meta:
        db_table = "message"
        
    def __str__(self):
        return self.subject