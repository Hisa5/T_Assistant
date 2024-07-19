# chatbot/urls.py
from django.urls import path
from .views import EntryLLMView  # Solo importa EntryLLMView si TechnicalQueryView no existe

urlpatterns = [
    path('entry-llm/', EntryLLMView.as_view(), name='entry_llm'),
    # Si tienes otras vistas, agrégalas aquí
]
