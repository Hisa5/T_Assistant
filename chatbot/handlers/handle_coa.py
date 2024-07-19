# chatbot/handlers/handle_coa.py
import requests

def handle_coa(query):
    # Aquí realizarías la llamada a la API de OpenAI para el LLM de COA
    response = {"reply": f"COA response to: {query}"}
    return response
