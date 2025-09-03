from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class GerenteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin para verificar se o usuário é gerente ou administrador"""
    
    def test_func(self):
        return self.request.user.cargo in ['GERENTE', 'ADMIN']
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acesso negado. Apenas gerentes podem acessar esta página.')
        return redirect('core:dashboard')


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo == 'ADMIN'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('core:dashboard')


class CaixaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cargo in ['CAIXA', 'GERENTE', 'ADMIN']
    
    def handle_no_permission(self):
        messages.error(self.request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('core:dashboard')


# Funções auxiliares para verificar permissões
def is_gerente(user):
    return user.cargo in ['GERENTE', 'ADMIN']


def is_admin(user):
    return user.cargo == 'ADMIN'


def is_caixa(user):
    return user.cargo in ['CAIXA', 'GERENTE', 'ADMIN']


def can_manage_mesas(user):
    return is_gerente(user)


def can_manage_funcionarios(user):
    return is_gerente(user)


def can_view_relatorios(user):
    return is_caixa(user)


def can_manage_system(user):
    return is_admin(user)
