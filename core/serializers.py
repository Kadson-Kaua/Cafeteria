from rest_framework import serializers
from .models import Categoria, Produto, Mesa, Comanda, ItemComanda
from users.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'categoria', 'categoria_nome', 'ativo', 'created_at']

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'

class ItemComandaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_preco = serializers.DecimalField(source='produto.preco', max_digits=8, decimal_places=2, read_only=True)
    
    class Meta:
        model = ItemComanda
        fields = ['id', 'produto', 'produto_nome', 'produto_preco', 'quantidade', 'preco_unitario', 'total']

class ComandaSerializer(serializers.ModelSerializer):
    itens = ItemComandaSerializer(many=True, read_only=True, source='itemcomanda_set')
    mesa_numero = serializers.CharField(source='mesa.numero', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Comanda
        fields = ['id', 'codigo', 'status', 'origem', 'observacao', 'desconto_valor', 
                 'taxa_percentual', 'created_at', 'mesa', 'mesa_numero', 'usuario', 
                 'usuario_nome', 'itens', 'subtotal', 'total_geral']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'cargo', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cargo']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
