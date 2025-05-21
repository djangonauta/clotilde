import uuid

from django.db import models


class Automacao(models.Model):
    class Status(models.IntegerChoices):
        INICIADA = 1
        FINALIZADA = 2
        ERRO = 3

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=Status, default=Status.INICIADA)
    stack_trace = models.TextField(blank=True)
    porcentagem = models.IntegerField(default=0)
    enviada = models.BooleanField(default=False)
