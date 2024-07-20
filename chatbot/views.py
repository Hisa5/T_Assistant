# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        # Aquí va la lógica para procesar el mensaje y obtener la respuesta
        response_message = "Esta es una respuesta simulada."
        return Response({'response': response_message}, status=status.HTTP_200_OK)
        
        # # Obtener o crear el hilo del usuario
        # user_thread = thread_manager.get_thread(user_id)
        # if not user_thread:
        #     thread_manager.create_thread(user_id)
        #     user_thread = thread_manager.get_thread(user_id)

        # # Determinar el LLM activo
        # active_llm = user_thread.get_active_llm()

        # if "COA" in query:
        #     user_thread.set_active_llm('coa')
        # elif "IFU" in query:
        #     user_thread.set_active_llm('ifu')
        # else:
        #     user_thread.set_active_llm('rag')

        # # Delegar la consulta al LLM activo
        # response = self.handle_query(user_thread.get_active_llm(), query)
        # return Response(response, status=status.HTTP_200_OK)

    def handle_query(self, active_llm, query):
        if active_llm == 'coa':
            return handle_coa(query)
        elif active_llm == 'ifu':
            return handle_ifu(query)
        else:
            return handle_rag(query)
