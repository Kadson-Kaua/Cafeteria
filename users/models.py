from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    CARGO_CHOICES = [  
        ('CAIXA', 'Caixa'),
        ('GERENTE', 'Gerente'),
        ('ADMIN', 'Administrador'),
    ]    

    cargo = models.CharField(max_length=10, choices=CARGO_CHOICES, default='CAIXA')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.username} - {self.cargo}"