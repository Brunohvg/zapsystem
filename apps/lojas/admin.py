from django.contrib import admin
from .models import Loja
# Register your models here.
@admin.register(Loja)
class UsuarioLojaAdmin(admin.ModelAdmin):
    list_display = ['nome_loja', 'cnpj']
    search_fields = ['cnpj']  # Usando __ para buscar o campo 'nome' no modelo Usuario
