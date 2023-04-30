from django.db import models

from apps.cnpj_lookup.models import Empresa


class Socio(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='socios')
    nome = models.CharField(max_length=200)
    qualificacao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nome} ({self.empresa.razao_social})'
