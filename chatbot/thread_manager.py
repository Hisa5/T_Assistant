# chatbot/thread_manager.py

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import Thread
import openai

class ThreadManager:
    def __init__(self):
        self.client = openai
        self.client.api_key = settings.OPENAI_API_KEY

    def create_thread(self, user):
        openai_thread = self.client.beta.threads.create()
        thread = Thread.objects.create(user=user, thread_id=openai_thread.id)
        thread.update_last_activity()
        return thread

    def get_or_create_active_thread(self, user):
        try:
            thread = Thread.objects.filter(user=user).latest('created_at')
            if thread.last_activity < timezone.now() - timedelta(minutes=10):
                thread = self.create_thread(user)
        except Thread.DoesNotExist:
            thread = self.create_thread(user)
        return thread

    def delete_thread(self, user):
        Thread.objects.filter(user=user, is_active=True).update(is_active=False)

class UserThread:
    def __init__(self):
        self.active_llm = 'rag'  # Default LLM

    def set_active_llm(self, llm_type):
        self.active_llm = llm_type

    def get_active_llm(self):
        return self.active_llm

    def update_last_activity(self):
        self.last_activity = timezone.now()

thread_manager = ThreadManager()
