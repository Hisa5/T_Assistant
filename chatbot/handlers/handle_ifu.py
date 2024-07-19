# chatbot/handlers/handle_ifu.py
import requests

def handle_ifu(query):
    # Aquí realizarías la llamada a la API de OpenAI para el LLM de IFU
    response = {"reply": f"IFU response to: {query}"}
    return response
