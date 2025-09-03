# ☕ Café Control - Sistema de Gestão para Cafeteria

Um sistema completo de gestão para cafeteria desenvolvido em Django, com controle de produtos, comandas, pagamentos e usuários.

## 🚀 Funcionalidades

### 👥 Gestão de Usuários
- **Sistema de Login/Registro** - Autenticação segura
- **Controle de Acesso** - Diferentes níveis (Caixa, Gerente, Administrador)
- **Gestão de Funcionários** - CRUD completo com modais

### 📦 Gestão de Produtos
- **Categorias** - Organização por categorias
- **Produtos** - Cadastro com preços e descrições
- **Status Ativo/Inativo** - Controle de disponibilidade

### 🍽️ Sistema de Comandas
- **Criação de Comandas** - Mesa, Balcão ou Delivery
- **Adição de Itens** - Interface intuitiva com busca
- **Controle de Status** - Aberta, Fechada, Paga
- **Cálculo Automático** - Subtotal, descontos e taxas

### 💳 Sistema de Pagamento
- **Múltiplos Métodos** - Dinheiro, Cartão, PIX
- **Cálculo de Troco** - Automático
- **Validações** - Valor mínimo, campos obrigatórios
- **Liberação de Mesa** - Automática após pagamento

### 🏢 Gestão de Mesas
- **Status das Mesas** - Livre, Ocupada, Reservada
- **Controle de Ocupação** - Apenas para gerentes

### 📊 Dashboard
- **Resumo Financeiro** - Total faturado
- **Estatísticas** - Produtos ativos, comandas
- **Visão Geral** - Dados em tempo real

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5
- **Ícones**: Bootstrap Icons
- **API**: Django REST Framework
- **Banco de Dados**: SQLite (desenvolvimento)
- **Autenticação**: Django Auth System

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/cafe-control.git
cd cafe-control
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

### 7. Acesse o sistema
Abra seu navegador e acesse: `http://127.0.0.1:8000`

## 👤 Níveis de Acesso

### 🧑‍💼 Administrador
- Acesso total ao sistema
- Gestão de funcionários
- Visualização de relatórios financeiros
- Criação de contas de usuário

### 👨‍💼 Gerente
- Gestão de produtos e categorias
- Controle de mesas
- Acesso a comandas e pagamentos
- Dashboard completo

### 💰 Caixa
- Criação de comandas
- Processamento de pagamentos
- Visualização de produtos
- Dashboard básico

## 🗂️ Estrutura do Projeto

```
cafe-control/
├── cafeteria/              # Configurações do projeto
│   ├── settings.py        # Configurações Django
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # Configuração WSGI
├── core/                  # App principal
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Views web
│   ├── api_views.py      # Views da API
│   ├── serializers.py    # Serializers DRF
│   ├── permissions.py    # Controle de acesso
│   ├── urls.py           # URLs do app
│   ├── api_urls.py       # URLs da API
│   └── templates/        # Templates HTML
├── users/                 # App de usuários
│   ├── models.py         # Modelo User customizado
│   ├── views.py          # Views de autenticação
│   ├── api_views.py      # API de usuários
│   ├── serializers.py    # Serializers de usuários
│   ├── urls.py           # URLs de usuários
│   └── api_urls.py       # URLs da API de usuários
├── static/               # Arquivos estáticos
│   ├── css/             # Folhas de estilo
│   ├── js/              # JavaScript
│   └── images/          # Imagens
├── media/               # Uploads de arquivos
├── requirements.txt     # Dependências Python
├── manage.py           # Script de gerenciamento Django
└── README.md           # Este arquivo
```

## 🔌 API REST

O sistema possui uma API REST completa para integração com outros sistemas:

### Endpoints Principais

#### Autenticação
- `POST /api/users/auth/login/` - Login
- `POST /api/users/auth/register/` - Registro
- `GET /api/users/auth/profile/` - Perfil do usuário

#### Produtos
- `GET /api/core/produtos/` - Listar produtos
- `POST /api/core/produtos/` - Criar produto
- `GET /api/core/produtos/{id}/` - Detalhes do produto
- `PUT /api/core/produtos/{id}/` - Atualizar produto
- `DELETE /api/core/produtos/{id}/` - Excluir produto

#### Comandas
- `GET /api/core/comandas/` - Listar comandas
- `POST /api/core/comandas/` - Criar comanda
- `GET /api/core/comandas/{id}/` - Detalhes da comanda
- `POST /api/core/comandas/{id}/pagamento/` - Processar pagamento

#### Pagamentos
- `GET /api/core/pagamentos/` - Listar pagamentos
- `POST /api/core/pagamentos/` - Criar pagamento
- `GET /api/core/pagamentos/{id}/` - Detalhes do pagamento

#### Relatórios
- `GET /api/core/faturamento/` - Relatório de faturamento (apenas admin)

### Exemplo de Uso da API

```bash
# Login
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "senha123"}'

# Processar pagamento
curl -X POST http://localhost:8000/api/core/comandas/1/pagamento/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token seu_token_aqui" \
  -d '{
    "metodo": "PIX",
    "valor_pago": 50.00,
    "troco": 5.00
  }'
```

## 🚀 Deploy

### Desenvolvimento
```bash
python manage.py runserver
```

### Produção
Para deploy em produção, recomenda-se:

1. **Configurar variáveis de ambiente**
2. **Usar PostgreSQL ou MySQL**
3. **Configurar servidor web (Nginx + Gunicorn)**
4. **Configurar arquivos estáticos**
5. **Configurar SSL/HTTPS**

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- Email: seu-email@exemplo.com

## 🙏 Agradecimentos

- Django Documentation
- Bootstrap Team
- Comunidade Python/Django

---

**Desenvolvido com ❤️ para facilitar a gestão de cafeterias**
