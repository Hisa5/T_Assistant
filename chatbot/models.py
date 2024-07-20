# chatbot/models.py

from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

User = get_user_model()

class Query(models.Model):
    QUERY_TYPE_CHOICES = [
        ('TECH', 'Technical Inquiry'),
        ('IFU', 'IFU Document Request'),
        ('COA', 'COA Document Request'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    query_type = models.CharField(max_length=4, choices=QUERY_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    thread_id = models.CharField(max_length=255, default=uuid.uuid4)  # Agregar un valor predeterminado

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()
