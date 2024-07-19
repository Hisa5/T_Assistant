# T_Assistant/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/documents/', include('documents.urls')),
]
