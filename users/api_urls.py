from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'usuarios', api_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/register/', api_views.register_user, name='api_register'),
    path('auth/login/', api_views.login_user, name='api_login'),
    path('auth/profile/', api_views.user_profile, name='api_profile'),
]
