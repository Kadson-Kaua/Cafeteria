from django.db import models
from django.utils.text import slugify
from users.models import User
# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
        db_table = 'categoria_produto'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Produto(models.Model): 
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
        

class Mesa(models.Model):
    STATUS_CHOICES = [
        ('LIVRE', 'Livre'),
        ('OCUPADA', 'Ocupada'),
        ('RESERVADA', 'Reservada')
    ]

    numero = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='LIVRE')

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']

    def __str__(self):
        return f"Mesa {self.numero} - {self.get_status_display()}"


class Comanda(models.Model):
    STATUS_CHOICES = [
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'Fechada'),
        ('PAGA', 'Paga'),
    ]
    ORIGEM_CHOICES = [
        ('MESA', 'Mesa'),
        ('BALCAO', 'Balcao'),
        ('VIAGEM', 'Viagem'),
    ]

    codigo = models.IntegerField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABERTA')
    origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES, default='MESA')
    observacao = models.TextField(blank=True)
    desconto_valor = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    taxa_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    mesa = models.ForeignKey(Mesa,  on_delete=models.CASCADE, null=True, blank=True)  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    pagamento = models.OneToOneField('Pagamento', on_delete=models.SET_NULL, null=True, blank=True, related_name='comanda_pagamento')  

    class Meta:
        verbose_name = 'Comanda'
        verbose_name_plural = 'Comandas'
        ordering = ['-created_at']
    
    @property
    def subtotal(self):
        """ Calcula o subtotal dos items da comanda """
        total = 0
        for item in self.itemcomanda_set.all():
            total+= item.total
        return total

    @property
    def total_geral(self):
        """ Calcula o total geral com desconto """
        subtotal = self.subtotal
        if self.desconto_valor:
            subtotal -= self.desconto_valor
        
        if self.taxa_percentual:
            taxa_valor = subtotal * (self.taxa_percentual / 100)
            subtotal += taxa_valor

        return subtotal

    def __str__(self):
        return f"Comanda {self.codigo} - {self.get_status_display()}"


class ItemComanda(models.Model):
    quantidade = models.IntegerField()
    observacao = models.TextField(blank=True)

    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Item da Comanda'
        verbose_name_plural = 'Itens da Comanda'
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x R$ {self.produto.preco}"

    @property
    def preco_unitario(self):
        """Retorna o preço atual do produto"""
        return self.produto.preco

    @property
    def total(self):
        """Calcula o total do item (quantidade * preço do produto)"""
        if self.quantidade is None or self.produto is None:
            return 0
        total = self.quantidade * self.produto.preco   
        return total   


class Pagamento(models.Model):
    METODOS_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO', 'Cartao'),
        ('PIX', 'Pix'),
    ]

    valor = models.DecimalField(max_digits=8, decimal_places=2)
    metodo = models.CharField(max_length=10, choices=METODOS_CHOICES, default='DINHEIRO')
    troco = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='pagamentos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pagamento {self.id} - R$ {self.valor} ({self.get_metodo_display()})"