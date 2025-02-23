from django.db import models
from medical_records.models import MedicalRecord
from django.contrib.auth.models import User

class Checklist(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField()

    class Meta:
        db_table = "checklist"

    def __str__(self):
        return f"Checklist for Record {self.record.id}"