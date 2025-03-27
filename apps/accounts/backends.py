from django.contrib.auth.backends import ModelBackend
from .models import Usuario

class EmailBackend(ModelBackend):
    """
    Backend de autenticação que utiliza o email em vez do username.
    
    Permite que os usuários se autentiquem utilizando seu email e senha.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica o usuário baseado no email e senha.
        
        :param username: O email do usuário.
        :param password: A senha fornecida.
        :return: Instância do usuário se as credenciais forem válidas; caso contrário, None.
        """
        try:
            # Tenta encontrar o usuário pelo email
            usuario = Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            return None
        
        # Verifica se a senha informada está correta
        if usuario.check_password(password):
            return usuario
        return None

    def get_user(self, user_id):
        """
        Retorna o usuário baseado no ID.
        
        :param user_id: ID do usuário.
        :return: Instância do usuário ou None se não existir.
        """
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
