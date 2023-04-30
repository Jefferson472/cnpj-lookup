from django.db import models


class Empresa(models.Model):
    cnpj = models.CharField(max_length=14, unique=True)
    razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cnae_principal = models.CharField(max_length=10)
    inscricao_estadual = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.razao_social} ({self.cnpj})'
