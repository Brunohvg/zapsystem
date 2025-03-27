"""
URLs do app 'usuarios'
-----------------------
Este arquivo configura as rotas (URLs) relacionadas às funcionalidades de usuários,
como registro, listagem, edição, exclusão, login, logout, recuperação e redefinição de senha.

Cada rota utiliza uma view correspondente definida em views.py e está
associada a um nome único (name) que facilita sua referência em templates e redirecionamentos.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

        
    # Rota para o login do usuário
    path('login/', views.logar, name='login'),
    # Rota para registrar um novo usuário
    path('registrar/', views.registrar, name='registrar'),
    
    # Rota para exibir a lista de usuários cadastrados
    #path('lista/', views.lista_usuarios, name='lista_usuarios'),
    
    # Rota para editar os dados de um usuário específico
    #path('editar/<int:id>/', views.edita_usuario, name='editar_usuario'),
    
    # Rota para eliminar um usuário (com confirmação via template)
    #path('eliminar/<int:id>/', views.elimina_usuario, name='eliminar_usuario'),
    
    # Rota para visualizar os detalhes de um usuário
    #path('detalhes/<int:id>/', views.detalle_usuario, name='detalhes_usuario'),

    # Rota para o logout do usuário (usando a view logout_user)
    #path('logout/', views.logout_user, name='logout'),
    
    # Rota para iniciar o processo de recuperação de senha
    #path('recuperar-senha/', views.recupera_senha, name='recuperar_senha'),
    
    # Rota para redefinir a senha via link enviado por email
    #path('resetar-senha/<uidb64>/<token>/', views.redefinir_senha, name='resetar_senha'),
    #path('perfil/', views.config_conta, name='config_conta')
]
