from django.db import models
from entities.models import Entity
from medical_records.models import MedicalRecord

class Attachment(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    url = models.CharField(max_length=250)

    def __str__(self):
        return f"Attachment {self.id} for {self.entity}"
    class Meta:
        db_table = "attachments"