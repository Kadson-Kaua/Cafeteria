from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('funcionarios/', views.FuncionariosListView.as_view(), name='funcionarios'),
    path('funcionarios/editar/<int:pk>/', views.EditarFuncionarioView.as_view(), name='editar_funcionario'),
    path('funcionarios/deletar/<int:pk>/', views.DeletarFuncionarioView.as_view(), name='deletar_funcionario'),
]