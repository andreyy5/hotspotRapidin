from django.db import models


class Cliente(models.Model):
    """Modelo para armazenar dados de clientes localmente"""
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'hotspot_cliente'

    def __str__(self):
        return f"{self.nome} - {self.cpf_cnpj}"
