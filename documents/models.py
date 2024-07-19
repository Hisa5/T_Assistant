from django.db import models

class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ('IFU', 'Instrucciones de Uso'),
        ('COA', 'Certificado de Análisis'),
    ]
    doc_type = models.CharField(max_length=3, choices=DOC_TYPE_CHOICES)
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.url}"
