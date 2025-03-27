from django.contrib import admin
from apps.accounts.models import Usuario, UsuarioLoja

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email']
    search_fields = ['nome', 'email']
    
@admin.register(UsuarioLoja)
class UsuarioLojaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'loja', 'data_vinculo']
    search_fields = ['usuario__nome', 'data_vinculo']  # Usando __ para buscar o campo 'nome' no modelo Usuario
