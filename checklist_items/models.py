from django.db import models
from checklists.models import Checklist
from checklist_types.models import ChecklistType

class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='checklistItems')
    type = models.ForeignKey(ChecklistType, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    due_date = models.DateField()
    task_status = models.IntegerField()
    complete_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "checklist_item"

    def __str__(self):
        return f"{self.title}"