from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth import login
from .models import User
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.permissions import AdminRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('core:dashboard')
    redirect_authenticated_user = True

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

class FuncionariosListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/funcionarios.html'
    context_object_name = 'funcionarios'
    ordering = ['first_name', 'last_name']

    def get_queryset(self):
        return User.objects.all().exclude(is_superuser=True)

class EditarFuncionarioView(AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'users/editar_funcionario.html'
    fields = ['cargo']
    success_url = reverse_lazy('users:funcionarios')
    
    def form_valid(self, form):
        form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Cargo do funcionário {self.object.get_full_name()} atualizado com sucesso!'
            })
        messages.success(self.request, f'Cargo do funcionário {self.object.get_full_name()} atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Dados inválidos'
            })
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cargo do Funcionário'
        return context

class DeletarFuncionarioView(AdminRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:funcionarios')
    
    def delete(self, request, *args, **kwargs):
        funcionario = self.get_object()
        nome = funcionario.get_full_name() or funcionario.username
        
        if funcionario == request.user:
            messages.error(request, 'Você não pode deletar sua própria conta!')
            return redirect('users:funcionarios')

        if funcionario.cargo == 'ADMIN' and User.objects.filter(cargo='ADMIN').count() <= 1:
            messages.error(request, 'Não é possível deletar o último administrador!')
            return redirect('users:funcionarios')
        
        funcionario.delete()
        messages.success(request, f'Funcionário {nome} removido com sucesso!')
        return redirect('users:funcionarios')
