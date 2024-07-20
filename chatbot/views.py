# chatbot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .thread_manager import thread_manager, UserThread
import openai
from django.conf import settings
from .handlers.handle_coa import handle_coa
from .handlers.handle_ifu import handle_ifu
from .handlers.handle_rag import handle_rag

class ChatbotEntryView(APIView):
    def __init__(self):
        self.client = openai
        self.client.api_key = settings.OPENAI_API_KEY
        self.permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        user = request.user

        # Obtener o crear el hilo del usuario
        thread = thread_manager.get_or_create_active_thread(user)

        # Actualizar la última actividad del hilo
        thread.update_last_activity()

        # Clasificar la consulta y obtener la respuesta
        response_message = self.process_user_query(message, user)
        return Response({'response': str(response_message)}, status=status.HTTP_200_OK)  # Asegurarse de que la respuesta sea una cadena

    def classify_query(self, query):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente que clasifica consultas de usuarios. Cuando te soliciten un COA tu respuesta va a ser exclusivamente 'COA', cuando soliciten un documento IFU tu respuesta va a ser 'IFU', y 'CT' cuando te hagan una consulta técnica."},
                {"role": "user", "content": f"Clasifica la siguiente consulta como 'Consulta Técnica', 'COA' o 'IFU': {query}"}
            ],
           
        )
        classification = response.choices[0].message.content.strip()
        return classification

    def process_user_query(self, query, user):
        thread = thread_manager.get_or_create_active_thread(user)
        user_thread = UserThread()  # Crear instancia de UserThread
        active_llm = self.classify_query(query)
        user_thread.set_active_llm(active_llm)
        
        if user_thread.get_active_llm() == 'COA':
            return handle_coa(query)
        elif user_thread.get_active_llm() == 'IFU':
            return handle_ifu(query)
        else:
            return handle_rag(query)
