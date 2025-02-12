from django.db import models

class ChecklistType(models.Model):
    type_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.type_desc
    
    class Meta:
        db_table = "checklist_type"