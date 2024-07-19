# documents/urls.py
from django.urls import path
from .views import COAView, IFUView

urlpatterns = [
    path('coa/', COAView.as_view(), name='coa'),
    path('ifu/', IFUView.as_view(), name='ifu'),
]
