from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # URLs de Produtos
    path('produtos/', views.ProdutoListView.as_view(), name='produtos'),
    path('produtos/adicionar/', views.ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('produtos/editar/<int:pk>/', views.ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/excluir/<int:pk>/', views.ProdutoDeleteView.as_view(), name='produto_delete'),
    
    # URLs de Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categorias'),
    path('categorias/adicionar/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria_detail'),
    path('categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/excluir/<int:pk>/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    
    # Comandas (página de pedidos)
    path('comandas/', views.ComandaListagemView.as_view(), name='comandas'),
    path('comandas/<int:pk>/', views.ComandaListView.as_view(), name='comanda_detail'),
    path('comandas/criar/', views.ComandaCreateView.as_view(), name='criar_comanda'),
    
    # Pedidos (lista de comandas)
    path('pedidos/', views.PedidosView.as_view(), name='pedidos'),
    path('pedidos/<int:pk>/', views.PedidosDetailView.as_view(), name='pedidos_detail'),
    path('pedidos/<int:comanda_id>/adicionar/<int:produto_id>/', views.AdicionarItemView.as_view(), name='adicionar_item'),
    path('pedidos/<int:comanda_id>/finalizar/', views.FinalizarComandaView.as_view(), name='finalizar_comanda'),
    path('pedidos/<int:comanda_id>/enviar-cozinha/', views.EnviarCozinhaView.as_view(), name='enviar_cozinha'),
    path('pedidos/<int:comanda_id>/pagamento/', views.ProcessarPagamentoView.as_view(), name='processar_pagamento'),
    
    # Mesas (apenas gerente)
    path('mesas/', views.MesaListView.as_view(), name='mesas'),
    path('mesas/adicionar/', views.MesaCreateView.as_view(), name='mesa_create'),
    path('mesas/editar/<int:pk>/', views.MesaUpdateView.as_view(), name='mesa_update'),
    path('mesas/excluir/<int:pk>/', views.MesaDeleteView.as_view(), name='mesa_delete'),
]   
