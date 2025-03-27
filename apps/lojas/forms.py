from django import forms
from .models import Loja


class RegistroLojaForm(forms.ModelForm):
    """
    Formulário para registro de novas lojas.

    Inclui os campos personalizados 'nome', 'cnpj', 'endereco' e 'telefone',
    com atributos de CSS e placeholders para melhor usabilidade.
    """
    nome_loja = forms.CharField(
        label="Loja",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o nome da sua Loja",
            "id": "nome_loja"
        })
    )

    cnpj = forms.CharField(
        label="CNPJ",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu CNPJ",
            "id": "cnpj"
        })
    )

    endereco = forms.CharField(
        label="Endereço",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu endereço",
            "id": "endereco"
        })
    )

    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu telefone",
            "id": "telefone_loja"
        })
    )

    class Meta:
        model = Loja
        fields = ("nome_loja", "cnpj", "endereco", "telefone")