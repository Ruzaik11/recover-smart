from django.db import models

class Attachment(models.Model):
    entity = models.CharField(max_length=250)
    record_id = models.IntegerField()
    url = models.TextField()

    def __str__(self):
        return f"Attachment {self.id} for {self.entity}"
    class Meta:
        db_table = "attachments"