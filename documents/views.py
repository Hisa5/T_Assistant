# documents/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class COAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        # Implementa la lógica para manejar las consultas COA
        response_message = f"COA response to: {query}"
        return Response({'reply': response_message}, status=status.HTTP_200_OK)

class IFUView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        # Implementa la lógica para manejar las consultas IFU
        response_message = f"IFU response to: {query}"
        return Response({'reply': response_message}, status=status.HTTP_200_OK)
