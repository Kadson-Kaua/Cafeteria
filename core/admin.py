from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'created_at']
    search_fields = ['nome', 'descricao']
    list_filter = ['created_at']
    ordering = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'categoria', 'ativo', 'created_at']
    list_filter = ['categoria', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    list_editable = ['preco', 'ativo']
    ordering = ['nome']

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'status']
    list_filter = ['status']
    search_fildes = ['numero']

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'status', 'origem', 'mesa', 'usuario', 'created_at']
    list_filter = ['status', 'origem', 'created_at']
    search_fields = ['codigo', 'observacao']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'preco_unitario', 'total', 'comanda']
    list_filter = ['comanda', 'produto']
    search_fields = ['produto__nome', 'comanda__codigo']
    readonly_fields = ['preco_unitario', 'total']
    ordering = ['-id']  

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor', 'metodo', 'troco', 'comanda', 'usuario', 'created_at']
    list_filter = ['metodo', 'created_at']
    search_fields = ['comanda__codigo', 'usuario__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']