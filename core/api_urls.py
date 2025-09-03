from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Router para ViewSets
router = DefaultRouter()
router.register(r'categorias', api_views.CategoriaViewSet)
router.register(r'produtos', api_views.ProdutoViewSet)
router.register(r'mesas', api_views.MesaViewSet)
router.register(r'comandas', api_views.ComandaViewSet)
router.register(r'itens-comanda', api_views.ItemComandaViewSet)

# URLs da API
urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
    
    # Endpoints específicos
    path('produtos/<int:pk>/detalhes/', api_views.produto_detail, name='api_produto_detail'),
    path('faturamento/', api_views.faturamento_empresa, name='api_faturamento'),
]
