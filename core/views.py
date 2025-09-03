from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages
from .permissions import GerenteRequiredMixin, AdminRequiredMixin, CaixaRequiredMixin


class DashboardView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'core/dashboard.html'
    context_object_name = 'produtos'
    
    def get_queryset(self):
        return Produto.objects.filter(ativo=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        
        comandas_pagas = Comanda.objects.filter(status='PAGA')
        total_faturado = 0
        
        for comanda in comandas_pagas:
            total_faturado += comanda.total_geral
        
        context['total_faturado'] = total_faturado
        
        return context

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'core/produtos/produtos.html'
    context_object_name = 'produtos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Produto.objects.all()
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = 'core/produtos/produto_form.html'
    fields = ['nome', 'descricao', 'preco', 'categoria', 'ativo']
    success_url = reverse_lazy('core:produtos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Produto'
        return context

class ProdutoUpdateView(LoginRequiredMixin, UpdateView): 
    model = Produto
    template_name = 'core/produtos/produto_edit.html'
    fields = ['nome', 'descricao', 'preco', 'categoria', 'ativo']
    success_url = reverse_lazy('core:produtos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Produto'
        return context

class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'core/produtos/produto_delete.html'
    success_url = reverse_lazy('core:produtos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Produto'
        return context

class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'core/produtos/produto_detail.html'
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = self.object.produto_set.all()
        return context


class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'core/categorias/categorias.html'
    context_object_name = 'categorias'
    paginate_by = 12

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    template_name = 'core/categorias/categoria_form.html'
    fields = ['nome', 'descricao', 'ativo']
    success_url = reverse_lazy('core:categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Categoria'
        return context

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    template_name = 'core/categorias/categoria_form.html'
    fields = ['nome', 'descricao', 'ativo']
    success_url = reverse_lazy('core:categorias')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria'
        return context

class CategoriaDeleteView(LoginRequiredMixin, DeleteView): 
    model = Categoria
    template_name = 'core/categorias/categoria_delete.html'
    success_url = reverse_lazy('core:categorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Categoria'
        return context


class CategoriaDetailView(LoginRequiredMixin, DetailView):
    model = Categoria
    template_name = 'core/categorias/categoria_detail.html'
    context_object_name = 'categoria'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = self.object.produto_set.all()
        return context

class ComandaCreateView(LoginRequiredMixin, CreateView):
    model = Comanda
    template_name = 'core/comandas/criar_comanda.html'
    fields = ['origem', 'mesa', 'observacao']
    success_url = reverse_lazy('core:pedidos')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.codigo = Comanda.objects.count() + 1
        response = super().form_valid(form)
        
        if form.instance.mesa:
            form.instance.mesa.status = 'OCUPADA'
            form.instance.mesa.save()
        
        self.request.session['comanda_atual'] = self.object.id
        messages.success(self.request, f'Comanda {self.object.codigo} criada!')
        return redirect('core:comanda_detail', pk=self.object.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mesas'] = Mesa.objects.filter(status='LIVRE')
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'mesa' in form.fields:
            form.fields['mesa'].queryset = Mesa.objects.filter(status='LIVRE')
        return form

class ComandaListView(LoginRequiredMixin, DetailView):
    model = Comanda
    template_name = 'core/comandas/comanda_detail.html'
    context_object_name = 'comanda'
    
    def get_object(self):
        comanda_id = self.kwargs.get('pk')
        if comanda_id:
            return get_object_or_404(Comanda, id=comanda_id)
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['produtos'] = Produto.objects.filter(ativo=True)
            context['categorias'] = Categoria.objects.filter(ativo=True)
            context['itens_comanda'] = self.object.itemcomanda_set.all()
        return context

class ComandaListagemView(LoginRequiredMixin, ListView):
    model = Comanda
    template_name = 'core/comandas/listar_comandas.html'
    context_object_name = 'comandas'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Comanda.objects.filter(usuario=self.request.user)

class PedidosDetailView(LoginRequiredMixin, DetailView):
    model = Comanda
    template_name = 'core/pedidos/pedidos.html'
    context_object_name = 'comanda'
    
    def get_object(self):
        comanda_id = self.kwargs.get('pk') or self.request.session.get('comanda_atual')
        if comanda_id:
            return get_object_or_404(Comanda, id=comanda_id)
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.filter(ativo=True)
        context['categorias'] = Categoria.objects.filter(ativo=True)
        context['itens_comanda'] = self.object.itemcomanda_set.all() if self.object else []
        return context

class AdicionarItemView(LoginRequiredMixin, CreateView):
    model = ItemComanda
    template_name = 'core/pedidos/adicionar_item.html'
    fields = ['quantidade', 'observacao']
    
    def form_valid(self, form):
        """Processa quando formulário é válido"""
        comanda_id = self.kwargs.get('comanda_id')
        produto_id = self.kwargs.get('produto_id')
        
        comanda = get_object_or_404(Comanda, id=comanda_id)
        produto = get_object_or_404(Produto, id=produto_id)
        
        form.instance.comanda = comanda
        form.instance.produto = produto
        
        item_existente = ItemComanda.objects.filter(
            comanda=comanda, 
            produto=produto
        ).first()
        
        if item_existente:
            item_existente.quantidade += form.instance.quantidade
            item_existente.save()
            messages.success(self.request, f'{produto.nome} adicionado à comanda!')
        else:
            form.save()
            messages.success(self.request, f'{produto.nome} adicionado à comanda!')
        
        return redirect('core:comanda_detail', pk=comanda_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs.get('produto_id')
        context['produto'] = get_object_or_404(Produto, id=produto_id)
        return context

class FinalizarComandaView(LoginRequiredMixin, View):
    def post(self, request, comanda_id):
        comanda = get_object_or_404(Comanda, id=comanda_id)
        comanda.status = 'FECHADA'
        comanda.save()
        
        if comanda.mesa:
            comanda.mesa.status = 'LIVRE'
            comanda.mesa.save()
        
        request.session.pop('comanda_atual', None)
        messages.success(request, f'Comanda {comanda.codigo} finalizada!')
        return redirect('core:comandas')

class ProcessarPagamentoView(LoginRequiredMixin, View):
    def get(self, request, comanda_id):
        comanda = get_object_or_404(Comanda, id=comanda_id)
        return render(request, 'core/pagamento/processar_pagamento.html', {
            'comanda': comanda
        })
    
    def post(self, request, comanda_id):
        comanda = get_object_or_404(Comanda, id=comanda_id)
        
        metodo = request.POST.get('metodo')
        valor_pago = request.POST.get('valor_pago')
        troco = request.POST.get('troco', 0)
        
        if not metodo or not valor_pago:
            messages.error(request, 'Preencha todos os campos obrigatórios!')
            return redirect('core:processar_pagamento', comanda_id=comanda_id)
        
        try:
            valor_pago = float(valor_pago)
            troco = float(troco) if troco else 0
        except ValueError:
            messages.error(request, 'Valores inválidos!')
            return redirect('core:processar_pagamento', comanda_id=comanda_id)
        
        if valor_pago < comanda.total_geral:
            messages.error(request, 'Valor pago é menor que o total da comanda!')
            return redirect('core:processar_pagamento', comanda_id=comanda_id)
        
        pagamento = Pagamento.objects.create(
            valor=valor_pago,
            metodo=metodo,
            troco=troco,
            comanda=comanda,
            usuario=request.user
        )
        
        comanda.pagamento = pagamento
        comanda.status = 'PAGA'
        comanda.save()
        
        if comanda.mesa:
            comanda.mesa.status = 'LIVRE'
            comanda.mesa.save()
        
        request.session.pop('comanda_atual', None)
        
        messages.success(request, f'Pagamento processado com sucesso! Comanda {comanda.codigo} paga.')
        return redirect('core:pedidos')

class EnviarCozinhaView(LoginRequiredMixin, View):
    def post(self, request, comanda_id):
        comanda = get_object_or_404(Comanda, id=comanda_id)
        
        if not comanda.itemcomanda_set.exists():
            messages.error(request, 'Não é possível enviar uma comanda vazia para a cozinha!')
            return redirect('core:comanda_detail', pk=comanda_id)
        
        messages.success(request, f'Comanda {comanda.codigo} enviada para a cozinha!')
        return redirect('core:pedidos')

class PedidosView(LoginRequiredMixin, View):
    def get(self, request):
        comandas = Comanda.objects.filter(usuario=request.user).order_by('-created_at')
        return render(request, 'core/pedidos/pedidos.html', {'comandas': comandas})

class MesaListView(GerenteRequiredMixin, ListView):
    model = Mesa
    template_name = 'core/mesas/mesas.html'
    context_object_name = 'mesas'
    ordering = ['numero']

class MesaCreateView(GerenteRequiredMixin, CreateView):
    """Criar nova mesa (apenas gerente)"""
    model = Mesa
    template_name = 'core/mesas/mesa_form.html'
    fields = ['numero', 'status']
    success_url = reverse_lazy('core:mesas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adicionar Mesa'
        return context

class MesaUpdateView(GerenteRequiredMixin, UpdateView):
    """Editar mesa (apenas gerente)"""
    model = Mesa
    template_name = 'core/mesas/mesa_form.html'
    fields = ['numero', 'status']
    success_url = reverse_lazy('core:mesas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Mesa'
        return context

class MesaDeleteView(GerenteRequiredMixin, DeleteView):
    """Excluir mesa (apenas gerente)"""
    model = Mesa
    template_name = 'core/mesas/mesa_delete.html'
    success_url = reverse_lazy('core:mesas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Excluir Mesa'
        return context