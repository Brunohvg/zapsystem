from gzip import READ
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
from django.conf import settings
from django.contrib import messages

# Configuração do logger
logger = logging.getLogger('usuarios')

# Definir o template base
TEMPLATE_NAME = 'accounts/base_auth.html'


def logar(request):
    """
    Função para o login do usuário. Valida as credenciais e loga o usuário.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            usuario = authenticate(request, username=email, password=senha)
            if usuario is not None:
                login(request, usuario)
                logger.info(f"Usuário {email} logado com sucesso.")
                return redirect("dashboard:index")
            else:
                logger.warning(f"Tentativa de login falha para {email}.")
                form.add_error("email", "Email ou senha incorretos.")
                form.add_error("senha", "")
    else:
        form = LoginForm()

    return render(request, template_name=TEMPLATE_NAME, context={"form": form})


def registrar(request):
    """
    Função para registrar um novo usuário e loja. Envia um e-mail de confirmação.
    """
    if request.method == 'POST':
        form_usuario = RegistroUsuarioForm(request.POST)
        form_loja = RegistroLojaForm(request.POST)

        if form_usuario.is_valid() and form_loja.is_valid():
            # Cria o usuário e a loja
            usuario = form_usuario.save()
            loja = form_loja.save()

            # Vincula o usuário à loja
            vincular_usuario_a_loja(usuario, loja)

            # Envia o e-mail de confirmação
            enviar_email_confirmacao(usuario, request)

            logger.info(f"Novo usuário registrado: {usuario.email}, Loja: {loja.nome_loja}")
            return redirect('accounts:login')
        else:
            messages.error(request, 'ERRO USUARIO JA EXISTE', extra_tags='error')
            logger.warning("Falha ao registrar usuário. Dados inválidos.")
    else:
        form_usuario = RegistroUsuarioForm()
        form_loja = RegistroLojaForm()

    return render(request, template_name=TEMPLATE_NAME, context={'form': form_usuario, 'loja_form': form_loja})




def vincular_usuario_a_loja(usuario, loja):
    """
    Função para vincular um usuário a uma loja. Cria uma relação de 1:1 entre eles.
    """
    if not UsuarioLoja.objects.filter(usuario=usuario, loja=loja).exists():
        UsuarioLoja.objects.create(usuario=usuario, loja=loja)
        logger.info(f"Usuário {usuario.email} vinculado à loja {loja.nome_loja}.")
    else:
        logger.warning(f"Usuário {usuario.email} já está vinculado à loja {loja.nome_loja}.")


def enviar_email_confirmacao(usuario, request):
    """
    Função para enviar um e-mail de confirmação após o registro de um novo usuário.
    """
    token = default_token_generator.make_token(usuario)
    uid = usuario.pk
    confirm_url = f"http://{get_current_site(request).domain}/confirmar-email/{uid}/{token}/"

    # Renderiza o template HTML do e-mail de confirmação
    html_message = render_to_string('accounts/confirmacao_email.html', {
        'confirm_url': confirm_url,
        'client_name': usuario.nome,  # Nome do usuário
        'year': 2025
    })

    # Configura o e-mail e envia
    email_message = EmailMessage(
        'Confirmação de E-mail',
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email]
    )
    email_message.content_subtype = "html"  # Definir conteúdo como HTML
    email_message.send(fail_silently=False)

    logger.info(f"E-mail de confirmação enviado para {usuario.email}.")


def confirmar_email(request, uidb64, token):
    """
    Função para confirmar o e-mail do usuário. Marca o usuário como ativo.
    """
    try:
        usuario = Usuario.objects.get(pk=uidb64)
    except Usuario.DoesNotExist:
        logger.warning("Usuário não encontrado para confirmação de e-mail.")
        return redirect('accounts:login')
    
    if not default_token_generator.check_token(usuario, token):
        logger.warning(f"Token inválido para o usuário {usuario.email}.")
        return redirect('accounts:login')
    
    usuario.is_active = True  # Marca o usuário como ativo
    usuario.save()
    logger.info(f"Email confirmado para o usuário {usuario.email}.")
    return redirect('accounts:login')


def recuperar_senha(request):
    """
    Função para recuperar a senha, gerando um link de redefinição.
    """
    if request.method == "POST":
        form = EsqueciSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                usuario = Usuario.objects.get(email=email)
                token = default_token_generator.make_token(usuario)
                uid = usuario.pk
                reset_url = f"http://{get_current_site(request).domain}/resetar-senha/{uid}/{token}/"
                enviar_email_redefinicao(usuario, reset_url)
                return redirect('accounts:login')
            except Usuario.DoesNotExist:
                form.add_error("email", "Usuário não encontrado.")
    else:
        form = EsqueciSenhaForm()

    return render(request, template_name=TEMPLATE_NAME, context={'form': form})


def enviar_email_redefinicao(usuario, reset_url):
    """
    Função para enviar um e-mail com o link para redefinição de senha.
    """
    html_message = render_to_string('accounts/redefinicao_senha.html', {
        'reset_url': reset_url,
        'client_name': usuario.nome,  # Nome do usuário
        'year': 2025
    })

    email_message = EmailMessage(
        'Redefinição de Senha',
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email]
    )
    email_message.content_subtype = "html"  # Definir conteúdo como HTML
    email_message.send(fail_silently=False)

    logger.info(f"E-mail de redefinição de senha enviado para {usuario.email}.")


def redefinir_senha(request, uidb64, token):
    """
    Função para redefinir a senha do usuário.
    """
    try:
        usuario = Usuario.objects.get(pk=uidb64)
    except Usuario.DoesNotExist:
        logger.warning("Usuário não encontrado para redefinir senha.")
        return redirect('accounts:login')
    
    if not default_token_generator.check_token(usuario, token):
        logger.warning(f"Token inválido para o usuário {usuario.email}.")
        return redirect('accounts:login')

    if request.method == "POST":
        form = NovaSenhaForm(request.POST)
        if form.is_valid():
            nova_senha = form.cleaned_data["nova_senha"]
            usuario.set_password(nova_senha)
            usuario.save()
            logger.info(f"Senha redefinida com sucesso para o usuário {usuario.email}.")
            return redirect('accounts:login')
    else:
        form = NovaSenhaForm()

    return render(request, template_name=TEMPLATE_NAME, context={'form': form})


def deslogar(request):
    logout(request)
    logger.info("Usuário deslogado com sucesso.")
    return redirect('accounts:login')

def alterar_senha(request):
    if request.method == 'POST':
        form = NovaSenhaForm(request.POST)
        if form.is_valid():
            nova_senha = form.cleaned_data['nova_senha']
            usuario = request.user
            usuario.set_password(nova_senha)
            usuario.save()
            logger.info(f"Senha alterada com sucesso para o usuário {usuario.email}.")
            return redirect('accounts:login')
    else:
        form = NovaSenhaForm()
    
    return render(request, TEMPLATE_NAME, {'form': form})

def perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            logger.info(f"Perfil do usuário {usuario.email} atualizado.")
            return redirect('accounts:perfil')
    else:
        form = RegistroUsuarioForm(instance=usuario)
    
    return render(request, TEMPLATE_NAME, {'form': form})
