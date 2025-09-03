from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from .models import Categoria, Produto, Mesa, Comanda, ItemComanda, Pagamento
from .serializers import (
    CategoriaSerializer, ProdutoSerializer, MesaSerializer,
    ComandaSerializer, ItemComandaSerializer, PagamentoSerializer, ComandaComPagamentoSerializer
)

# ViewSets para CRUD completo
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Produto.objects.all()
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria__nome=categoria)
        return queryset

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ComandaViewSet(viewsets.ModelViewSet):
    queryset = Comanda.objects.all()
    serializer_class = ComandaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Comanda.objects.filter(usuario=self.request.user)

class ItemComandaViewSet(viewsets.ModelViewSet):
    queryset = ItemComanda.objects.all()
    serializer_class = ItemComandaSerializer
    permission_classes = [permissions.IsAuthenticated]

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pagamento.objects.filter(usuario=self.request.user)

# API Views para funcionalidades específicas
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def produto_detail(request, pk):
    """Endpoint para detalhes do produto com estoque"""
    try:
        produto = Produto.objects.get(pk=pk)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)
    except Produto.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def processar_pagamento_api(request, comanda_id):
    """Endpoint para processar pagamento via API"""
    try:
        comanda = Comanda.objects.get(id=comanda_id, usuario=request.user)
        
        # Verificar se comanda já foi paga
        if comanda.status == 'PAGA':
            return Response({'error': 'Comanda já foi paga'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obter dados do request
        metodo = request.data.get('metodo')
        valor_pago = request.data.get('valor_pago')
        troco = request.data.get('troco', 0)
        
        # Validar dados
        if not metodo or not valor_pago:
            return Response({'error': 'Método e valor são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            valor_pago = float(valor_pago)
            troco = float(troco) if troco else 0
        except ValueError:
            return Response({'error': 'Valores inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se valor pago é suficiente
        if valor_pago < comanda.total_geral:
            return Response({'error': 'Valor pago é menor que o total da comanda'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Criar pagamento
        pagamento = Pagamento.objects.create(
            valor=valor_pago,
            metodo=metodo,
            troco=troco,
            comanda=comanda,
            usuario=request.user
        )
        
        # Atualizar comanda
        comanda.pagamento = pagamento
        comanda.status = 'PAGA'
        comanda.save()
        
        # Liberar mesa se existir
        if comanda.mesa:
            comanda.mesa.status = 'LIVRE'
            comanda.mesa.save()
        
        return Response({
            'message': 'Pagamento processado com sucesso',
            'pagamento': PagamentoSerializer(pagamento).data,
            'comanda': ComandaComPagamentoSerializer(comanda).data
        }, status=status.HTTP_201_CREATED)
        
    except Comanda.DoesNotExist:
        return Response({'error': 'Comanda não encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def faturamento_empresa(request):
    """Endpoint para faturamento da empresa (apenas para dono)"""
    if request.user.cargo != 'ADMIN':
        return Response({'error': 'Acesso negado'}, status=status.HTTP_403_FORBIDDEN)
    
    # Cálculo do faturamento
    comandas_pagas = Comanda.objects.filter(status='PAGA')
    faturamento_total = comandas_pagas.aggregate(total=Sum('total_geral'))['total'] or 0
    
    # Estatísticas por origem
    faturamento_por_origem = comandas_pagas.values('origem').annotate(
        total=Sum('total_geral'),
        quantidade=Sum('id')
    )
    
    return Response({
        'faturamento_total': faturamento_total,
        'faturamento_por_origem': list(faturamento_por_origem),
        'total_comandas_pagas': comandas_pagas.count()
    })
