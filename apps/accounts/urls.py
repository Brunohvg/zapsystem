from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.logar, name='login'),
    path('registrar/', views.registrar, name='registrar'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('resetar-senha/<uidb64>/<token>/', views.redefinir_senha, name='redefinir_senha'),
    path('logout/', views.deslogar, name='logout'),  # Nova URL para logout
    path('confirmar-email/<uidb64>/<token>/', views.confirmar_email, name='confirmar_email'),  # Nova URL para confirmação de e-mail
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),  # Nova URL para alterar senha
    path('perfil/', views.perfil, name='perfil'),  # Nova URL para perfil do usuário
]
