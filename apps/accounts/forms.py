from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    """
    Formulário para registro de novos usuários.
    
    Estende o UserCreationForm do Django para incluir os campos personalizados
    'nome' e 'email', com atributos de CSS e placeholders para melhor usabilidade.
    """
    nome = forms.CharField(
        label="Nome",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu nome",
            "id": "nome"
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu email",
            "id": "email"
        })
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha",
            "id": "password1"
        })
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirme sua senha",
            "id": "password2"
        })
    )

    class Meta:
        model = Usuario
        fields = ("nome", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Salva o novo usuário após validar os dados.
        
        Garante que os campos email e nome sejam devidamente atribuídos.
        """
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data["email"]
        usuario.nome = self.cleaned_data["nome"]
        if commit:
            usuario.save()
        return usuario

class LoginForm(forms.Form):
    """
    Formulário para login de usuário.
    
    Valida a presença dos campos 'email' e 'senha'.
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu email",
            "id": "email"
        })
    )
    
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha",
            "id": "password"
        })
    )
    
    def clean_email(self):
        """
        Valida se o campo email não está vazio.
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Este campo é obrigatório")
        return email

    def clean_senha(self):
        """
        Valida se o campo senha não está vazio.
        """
        senha = self.cleaned_data.get('senha')
        if not senha:
            raise forms.ValidationError("Este campo é obrigatório")
        return senha

class EsqueciSenhaForm(forms.Form):
    """
    Formulário para solicitação de recuperação de senha.
    
    Apenas valida se o campo email foi preenchido e se possui um formato válido.
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu email",
            "id": "email",
        }),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Digite um email válido.'
        }
    )

    def clean_email(self):
        """
        Valida se o email foi preenchido.
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Este campo é obrigatório")
        return email

class NovaSenhaForm(forms.Form):
    """
    Formulário para redefinição de senha.
    
    Solicita que o usuário informe a nova senha e a confirmação, garantindo que
    ambas sejam iguais.
    """
    nova_senha = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite sua nova senha",
            "id": "nova_senha"
        }),
        error_messages={
            'required': 'Este campo é obrigatório.'
        }
    )

    confirmar_senha = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirme sua nova senha",
            "id": "confirmar_senha"
        }),
        error_messages={
            'required': 'Este campo é obrigatório.'
        }
    )

    def clean(self):
        """
        Valida se os campos 'nova_senha' e 'confirmar_senha' coincidem.
        """
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if nova_senha and confirmar_senha and nova_senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data
