from django.contrib import admin
from .models import Postagem, Usuario

@admin.register(Postagem)
class PostagemAdmin(admin.ModelAdmin):
    list_display = ('valor', 'data_hora')  # Campos que aparecerão na listagem
    list_filter = ('data_hora',)           # Filtros no painel
    search_fields = ('valor', 'descricao')
    
  
@admin.register(Usuario)
class ListUser(admin.ModelAdmin):
    list_display = ('nome', 'get_email', 'foto') 
    list_filter = ('nome', 'user__email')  
    search_fields = ('nome', 'user__email')  

    def get_email(self, obj):
        return obj.user.email 

    get_email.short_description = 'Email'  