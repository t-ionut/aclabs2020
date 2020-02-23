import uuid
from django.db import models

# Create your models here.
class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    priority = models.CharField(
        choices=[
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low")],
        default="LOW",
        max_length=10)
    due_date = models.DateField(null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "{text} @{time}".format(
            text=self.text,
            time=self.due_date
        )
