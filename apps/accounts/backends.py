from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        usuario = Usuario.objects.filter(email=email).first()
        if usuario and usuario.check_password(password):
            return usuario
        return None

    def get_user(self, user_id):
        return Usuario.objects.filter(pk=user_id).first()
