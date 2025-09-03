from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Router para ViewSets
router = DefaultRouter()
router.register(r'usuarios', api_views.UserViewSet)

# URLs da API de users
urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
    
    # Endpoints específicos
    path('auth/register/', api_views.register_user, name='api_register'),
    path('auth/login/', api_views.login_user, name='api_login'),
    path('auth/profile/', api_views.user_profile, name='api_profile'),
]
