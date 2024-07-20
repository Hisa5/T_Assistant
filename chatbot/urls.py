from django.urls import path
from .views import ChatbotEntryView

urlpatterns = [
    path('entry-llm/', ChatbotEntryView.as_view(), name='entry-llm'),
]
