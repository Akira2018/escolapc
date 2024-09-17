from django.contrib import admin
from .models import User, Escola  # Mantenha apenas uma importação
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import ClienteForm, EscolaForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .forms import EmprestimoLivroForm, EmprestimoVideoForm  # Importa os forms
from django.contrib import admin
from .forms import LivroForm
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied

from .models import (
    Autores, Editoras, Generos, Assuntos, Eventos, Livros, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'escola')

    # Crie dois fieldsets, um para superusuários e outro para usuários normais
    superuser_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),  # Inclui 'is_superuser' para superusuários
        ('Escola', {'fields': ('escola',)}),
    )

    normal_user_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff')}),  # Remove 'is_superuser' para usuários normais
        ('Escola', {'fields': ('escola',)}),
    )

    def get_fieldsets(self, request, obj=None):
        # Se o usuário logado for superusuário, use fieldsets com 'is_superuser'
        if request.user.is_superuser:
            return self.superuser_fieldsets
        # Caso contrário, use fieldsets sem 'is_superuser'
        return self.normal_user_fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(escola=request.user.escola) if request.user.escola else qs.none()

    def save_model(self, request, obj, form, change):
        # Se o usuário não for superusuário, ele não pode conceder status de superusuário
        if not request.user.is_superuser:
            # Impede a alteração do campo 'is_superuser' por um usuário não superusuário
            if 'is_superuser' in form.changed_data and obj.is_superuser:
                raise PermissionError("Somente superusuários podem conceder status de superusuário.")
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        # Oculta do menu principal
        return False

class BaseEscolaAdmin(admin.ModelAdmin):
    """
    Classe base para aplicar a lógica de filtragem e controle de campo de escola para usuários do grupo 'Gerentes'.
    """

    def get_queryset(self, request):
        # Obtem o queryset original
        qs = super().get_queryset(request)

        # Se o usuário é superusuário, ele vê todos os registros
        if request.user.is_superuser:
            return qs

        # Se o usuário pertence ao grupo 'Gerentes', filtra pela escola associada ao usuário
        if request.user.groups.filter(name='Gerentes').exists():
            return qs.filter(escola=request.user.escola)

        # Se não pertence a 'Gerentes' e não é superusuário, não pode ver nada
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        # Obtém o formulário original
        form = super(BaseEscolaAdmin, self).get_form(request, obj, **kwargs)

        # Se o usuário não for superusuário e pertence ao grupo 'Gerentes'
        if not request.user.is_superuser and request.user.groups.filter(name='Gerentes').exists():
            # Desabilita a seleção da escola
            if 'escola' in form.base_fields:
                form.base_fields['escola'].disabled = True  # Desabilita o campo
                form.base_fields['escola'].initial = request.user.escola  # Define a escola associada ao usuário

        return form

    def has_module_permission(self, request):
        # Superusuários têm acesso total
        if request.user.is_superuser:
            return True

        # Usuários do grupo 'Gerentes' têm permissão
        if request.user.groups.filter(name='Gerentes').exists():
            return True

        # Outros usuários não têm permissão
        return False

class AutoresAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('nome_autor', 'nacionalidade', 'biografia','get_nome_escola')
    search_fields = ('nome_autor',)
    list_filter = ('nacionalidade',)
    ordering = ('nome_autor',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class EditorasAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('nome_editora', 'pais','get_nome_escola')
    search_fields = ('nome_editora',)
    list_filter = ('pais',)
    ordering = ('nome_editora',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class GenerosAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('nome_genero','get_nome_escola')
    search_fields = ('nome_genero',)
    ordering = ('nome_genero',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class AssuntosAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('descr_assunto','get_nome_escola')
    search_fields = ('descr_assunto',)
    ordering = ('descr_assunto',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class EventosAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('nome_evento','data_evento','get_nome_escola')
    search_fields = ('nome_evento','data_evento')
    ordering = ('nome_evento','data_evento')

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class LivrosAdmin(admin.ModelAdmin):  # Alterado para admin.ModelAdmin
    list_display = ('titulo', 'get_nome_autor', 'isbn', 'edicao', 'ano_publicacao', 'qtlivros', 'get_nome_escola')
    search_fields = ('titulo', 'isbn')
    list_filter = ('titulo',)
    ordering = ('titulo',)

    def get_nome_autor(self, obj):
        return obj.nome_autor.nome_autor if obj.nome_autor else 'Autor não definido'
    get_nome_autor.short_description = 'Nome do Autor'

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola if obj.escola else 'Escola não definida'
    get_nome_escola.short_description = 'Nome da Escola'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Alunos').exists():
            # Permitir que os alunos visualizem apenas os livros da escola associada
            return qs.filter(escola=request.user.escola) if request.user.escola else qs.none()
        if request.user.is_superuser or request.user.groups.filter(name='Gerentes').exists():
            # Superusuários e gerentes podem ver todos os livros
            return qs
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Se o usuário for do grupo "Alunos", impedir o acesso à página de edição
        if request.user.groups.filter(name='Alunos').exists():
            raise PermissionDenied("Você não tem permissão para editar este item.")
        # Se o usuário não for superusuário, desabilitar a seleção de escola
        if not request.user.is_superuser:
            form.base_fields['escola'].disabled = True
            form.base_fields['escola'].initial = request.user.escola
        return form

    def save_model(self, request, obj, form, change):
        # Se o usuário não for superusuário, atribuir automaticamente a escola
        if not request.user.is_superuser:
            obj.escola = request.user.escola
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Bloquear permissão de edição para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        # Bloquear permissão de adição para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Bloquear permissão de exclusão para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_delete_permission(request, obj)

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class VideosAdmin(admin.ModelAdmin):  # Alterado para admin.ModelAdmin
    list_display = ('nome_video', 'ano_publicacao', 'colecao', 'qtvideos', 'estante', 'get_nome_escola')
    search_fields = ('nome_video', 'colecao')
    list_filter = ('nome_video', 'ano_publicacao')
    ordering = ('nome_video',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola if obj.escola else 'Escola não definida'
    get_nome_escola.short_description = 'Nome da Escola'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Alunos').exists():
            # Permitir que os alunos visualizem apenas os vídeos da escola associada
            return qs.filter(escola=request.user.escola) if request.user.escola else qs.none()
        if request.user.is_superuser or request.user.groups.filter(name='Gerentes').exists():
            # Superusuários e gerentes podem ver todos os vídeos
            return qs
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Se o usuário for do grupo "Alunos", impedir o acesso à página de edição
        if request.user.groups.filter(name='Alunos').exists():
            raise PermissionDenied("Você não tem permissão para editar este item.")
        # Se o usuário não for superusuário, desabilitar a seleção de escola
        if not request.user.is_superuser:
            form.base_fields['escola'].disabled = True
            form.base_fields['escola'].initial = request.user.escola
        return form

    def save_model(self, request, obj, form, change):
        # Se o usuário não for superusuário, atribuir automaticamente a escola
        if not request.user.is_superuser:
            obj.escola = request.user.escola
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Bloquear permissão de edição para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        # Bloquear permissão de adição para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Bloquear permissão de exclusão para o grupo "Alunos"
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_delete_permission(request, obj)

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class EscolaAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    list_display = ('nome_escola', 'nr_telefone', 'email', 'logradouro', 'bairro', 'cidade', 'estado', 'nr_imovel')
    search_fields = ('nome_escola', 'nr_telefone', 'email', 'logradouro', 'bairro', 'cidade', 'estado')
    ordering = ('nome_escola',)

    # Permissões para visualizar o modelo
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superusuário pode visualizar
        return False  # Não superusuários não podem visualizar

    # Permissões para adicionar
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True  # Superusuário pode adicionar
        return False  # Não superusuários não podem adicionar

    # Permissões para editar
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superusuário pode editar
        return False  # Não superusuários não podem editar

    # Permissões para deletar
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superusuário pode deletar
        return False  # Não superusuários não podem deletar

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class ClientesAdmin(BaseEscolaAdmin):
    list_display = ('nome_cliente', 'email', 'documento', 'nr_telefone', 'tipo_usuario', 'get_nome_escola')
    search_fields = ('nome_cliente', 'email', 'documento', 'nr_telefone', 'escola__nome_escola')  # Use o relacionamento correto
    list_filter = ('nome_cliente',)
    form = ClienteForm
    ordering = ('nome_cliente',)

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class ReservasAdmin(BaseEscolaAdmin):  # Herda de BaseEscolaAdmin
    list_display = ('get_titulo', 'get_nome_cliente', 'data_reserva', 'data_retirada', 'data_devolucao', 'get_nome_escola')
    search_fields = ('titulo__titulo', 'nome_cliente__nome_cliente')
    list_filter = ('data_reserva', 'data_retirada', 'data_devolucao')
    ordering = ('data_reserva',)

    def get_titulo(self, obj):
        return obj.titulo.titulo  # Corrige a chamada para o título
    get_titulo.short_description = 'Título do Livro/Vídeo'

    def get_nome_cliente(self, obj):
        return obj.nome_cliente.nome_cliente  # Corrige a chamada para nome_cliente
    get_nome_cliente.short_description = 'Nome do Cliente'

    def get_nome_escola(self, obj):
        return obj.titulo.escola.nome_escola  # Acessa o campo escola relacionado ao título
    get_nome_escola.short_description = 'Nome da Escola'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Se o usuário for superusuário, ele vê todas as reservas
        if request.user.is_superuser:
            return qs
        # Filtra as reservas para a escola do usuário logado
        if request.user.escola:
            return qs.filter(titulo__escola=request.user.escola)
        return qs.none()

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class EmprestimoLivroAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    form = EmprestimoLivroForm
    list_display = ('get_titulo', 'get_nome_cliente', 'get_qtlivros', 'data_emprestimo', 'data_devolucao', 'multa','get_nome_escola')
    search_fields = ('titulo__titulo', 'nome_cliente__nome_cliente', 'escola__nome_escola')
    list_filter = ('data_emprestimo', 'data_devolucao')
    ordering = ('data_emprestimo',)

    def get_titulo(self, obj):
        return obj.titulo.titulo
    get_titulo.short_description = 'Nome do Livro'

    def get_nome_cliente(self, obj):
        return obj.nome_cliente.nome_cliente
    get_nome_cliente.short_description = 'Nome do Cliente'

    def get_qtlivros(self, obj):
        return obj.titulo.qtlivros
    get_qtlivros.short_description = 'Qtdes de Livros'

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

class EmprestimoVideoAdmin(BaseEscolaAdmin):  # Agora herda de BaseEscolaAdmin
    form = EmprestimoVideoForm
    list_display = ('get_nome_video', 'get_nome_cliente', 'get_qtvideos', 'data_emprestimo', 'data_devolucao', 'multa','get_nome_escola')
    search_fields = ('nome_video__titulo', 'nome_cliente__nome_cliente')
    list_filter = ('data_emprestimo', 'data_devolucao')
    ordering = ('data_emprestimo',)

    def get_nome_video(self, obj):
        return obj.nome_video.nome_video
    get_nome_video.short_description = 'Nome do Vídeo'

    def get_nome_cliente(self, obj):
        return obj.nome_cliente.nome_cliente
    get_nome_cliente.short_description = 'Nome do Cliente'

    def get_qtvideos(self, obj):
        return obj.nome_video.qtvideos
    get_qtvideos.short_description = 'Quantidade de Vídeos'

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return False  # Apenas superusuário vê o menu
        return False  # Não superusuários não veem o menu

# Registro dos modelos
admin.site.register(Autores, AutoresAdmin)
admin.site.register(Editoras, EditorasAdmin)
admin.site.register(Generos, GenerosAdmin)
admin.site.register(Assuntos, AssuntosAdmin)
admin.site.register(Eventos, EventosAdmin)
admin.site.register(Livros, LivrosAdmin)
admin.site.register(Escola, EscolaAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Reservas, ReservasAdmin)
admin.site.register(EmprestimoLivro, EmprestimoLivroAdmin)
admin.site.register(EmprestimoVideo, EmprestimoVideoAdmin)
admin.site.register(User, CustomUserAdmin)
