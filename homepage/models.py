from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass


class Ticket(models.Model):
    NEW = 'New'
    INPROGRESS = 'In Progress'
    DONE = 'DONE'
    INVALID = 'Invalid'
    title = models.CharField(max_length=80)
    description = models.TextField()
    created_at = models.DateTimeField()
    status_options = [
        (NEW, 'New'),
        (INPROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid')
    ]
    status = models.CharField(max_length=80, choices=status_options, default=NEW)
    user_that_filed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='filed_by')
    user_assigned = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='assigned_user')
    completed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='completed')

        
