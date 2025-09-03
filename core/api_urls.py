from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'categorias', api_views.CategoriaViewSet)
router.register(r'produtos', api_views.ProdutoViewSet)
router.register(r'mesas', api_views.MesaViewSet)
router.register(r'comandas', api_views.ComandaViewSet)
router.register(r'itens-comanda', api_views.ItemComandaViewSet)
router.register(r'pagamentos', api_views.PagamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('produtos/<int:pk>/detalhes/', api_views.produto_detail, name='api_produto_detail'),
    path('comandas/<int:comanda_id>/pagamento/', api_views.processar_pagamento_api, name='api_processar_pagamento'),
    path('faturamento/', api_views.faturamento_empresa, name='api_faturamento'),
]
