from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/chatbot/', include('chatbot.urls')), 
    # Incluye otras rutas aquí
]
