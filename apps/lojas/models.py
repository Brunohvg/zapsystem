from django.db import models

class Loja(models.Model):
    nome_loja = models.CharField("Nome da Loja", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=20, unique=True)
    endereco = models.TextField("Endereço")
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return self.nome_loja
