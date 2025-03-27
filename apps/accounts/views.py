import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import RegistroUsuarioForm, LoginForm, EsqueciSenhaForm, NovaSenhaForm
from apps.lojas.forms import RegistroLojaForm 
from .models import Usuario, UsuarioLoja

# Configuração do logger específico para o app 'usuarios'
logger = logging.getLogger(None)

TEMPLATE_NAME = 'accounts/base_auth.html'

def logar(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            usuario = authenticate(request, username=email, password=senha)
            if usuario is not None:
                login(request, usuario)
                logger.info(f"Usuário {email} logado com sucesso.")
                return redirect("dashboard:index")  # Inclua o namespace antes do nome da view
            else:
                logger.warning(f"Tentativa de login falha para {email}. Credenciais incorretas.")
                form.add_error("email", "Email ou senha incorretos.")
                form.add_error("senha", "")
    else:
        form = LoginForm()
    return render(request, template_name=TEMPLATE_NAME, context={"form": form})
    
def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        loja_form = RegistroLojaForm(request.POST)

        if form.is_valid() and loja_form.is_valid():
            usuario = form.save()
            loja = loja_form.save()  # Salva a loja

            # Vincula o usuário à loja
            usuario_loja = UsuarioLoja.objects.create(usuario=usuario, loja=loja)

            logger.info(f"Novo usuário registrado: {usuario.email} (Loja: {loja.nome_loja})")
            return redirect('accounts:login')  # Redireciona para a página de login após o registro
        else:
            logger.warning("Falha ao registrar usuário. Dados inválidos.")

    else:
        form = RegistroUsuarioForm()
        loja_form = RegistroLojaForm()

    return render(
        request,
        template_name=TEMPLATE_NAME,
        context={'form': form, 'loja_form': loja_form}
    )

def atualizar(request, user_id : int):
    
    return render(request, template_name=TEMPLATE_NAME)

def listar_usuarios(request):
    pass

def listar_usuario(request, user_id : int):
    pass

def deletar(request, user_id : int):
    return render(request, template_name=TEMPLATE_NAME)


