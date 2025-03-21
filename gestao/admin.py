from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Escola, Livros, Videos, Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
from .models import Autores, Editoras, Generos, Eventos, Assuntos

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'escola')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Escola', {'fields': ('escola',)}),
    )

    def has_module_permission(self, request):
        """Oculta o menu de usuários para o grupo 'Gerentes'."""
        is_gerente = request.user.groups.filter(name='Gerentes').exists()
        if is_gerente and not request.user.is_superuser:
            return False
        return super().has_module_permission(request)

    def has_add_permission(self, request):
        """Impede que usuários do grupo 'Gerentes' adicionem usuários."""
        is_gerente = request.user.groups.filter(name='Gerentes').exists()
        if is_gerente and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        """Impede que usuários do grupo 'Gerentes' alterem usuários."""
        is_gerente = request.user.groups.filter(name='Gerentes').exists()
        if is_gerente and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Impede que usuários do grupo 'Gerentes' excluam usuários."""
        is_gerente = request.user.groups.filter(name='Gerentes').exists()
        if is_gerente and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

# ⚠️ Bloquear Gerentes de ver o menu de Grupos no Django Admin
class CustomGroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser  # Apenas superusuários podem ver o menu de grupos

    def has_add_permission(self, request):
        return request.user.is_superuser  # Apenas superusuários podem adicionar grupos

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Apenas superusuários podem modificar grupos

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Apenas superusuários podem excluir grupos

# Registra os modelos no Django Admin com as restrições
admin.site.register(CustomUser, CustomUserAdmin)
# Oculta os Grupos para usuários não superusuários
admin.site.unregister(Group)  # Remove a opção de Grupos do Django Admin
admin.site.register(Group, CustomGroupAdmin)  # Adiciona de volta com as restrições

def cadastro_escola(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = EscolaForm()
    return render(request, 'cadastro_escola.html', {'form': form})

def cadastro_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm()
    return render(request, 'gestao/cadastro_livro.html', {'form': form})

def cadastro_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_video')
    else:
        form = VideoForm()
    return render(request, 'gestao/cadastro_video.html', {'form': form})

def cadastro_reservas(request):
    if request.method == "POST":
        form = ReservasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = ReservasForm()
    return render(request, 'gestao/cadastro_reservas.html', {'form': form})

def cadastro_eventos(request):
    if request.method == "POST":
        form = EventosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listagem/lista_eventos')
    else:
        form = EventosForm()
    return render(request, 'gestao/cadastro_eventos.html', {'form': form})

def custom_admin_view(request):
        # Verifique se o usuário está nos grupos 'Gerentes' ou 'Alunos'
    user = request.user
    gerentes = user.groups.filter(name='Gerentes').exists()
    alunos = user.groups.filter(name='Alunos').exists()

    # Passe essas informações para o contexto
    context = {
        'gerentes': gerentes,
        'alunos': alunos,
    }
    return render(request, 'admin/custom_template.html', context)

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
    list_display = ('nome_evento','data_evento','local', 'get_nome_escola')
    search_fields = ('nome_evento','data_evento','local')
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

    # Exibir o nome do autor no list_display
    def get_nome_autor(self, obj):
        return obj.nome_autor.nome_autor if obj.nome_autor else 'Autor não definido'
    get_nome_autor.short_description = 'Nome do Autor'

    # Exibir o nome da escola no list_display
    def get_nome_escola(self, obj):
        return obj.escola.nome_escola if obj.escola else 'Escola não definida'
    get_nome_escola.short_description = 'Nome da Escola'

    # Definir o queryset com base no usuário logado
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusuários veem todos os registros
        if request.user.is_superuser:
            return qs

        # Usuários que não são superusuários visualizam apenas os livros da escola associada
        if request.user.escola:
            return qs.filter(escola=request.user.escola)

        # Se o usuário não tiver uma escola associada, retorna nenhum registro
        return qs.none()

    # Definir permissões de edição
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

    # Salvar o modelo com a escola associada ao usuário
    def save_model(self, request, obj, form, change):
        # Se o usuário não for superusuário, atribuir automaticamente a escola
        if not request.user.is_superuser:
            obj.escola = request.user.escola
        super().save_model(request, obj, form, change)

    # Definir permissões de edição para o grupo "Alunos"
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_change_permission(request, obj)

    # Bloquear permissão de adição para o grupo "Alunos"
    def has_add_permission(self, request):
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_add_permission(request)

    # Bloquear permissão de exclusão para o grupo "Alunos"
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_delete_permission(request, obj)

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        # Apenas superusuário deve ver o menu
        return request.user.is_superuser

class VideosAdmin(admin.ModelAdmin):  # Baseado em admin.ModelAdmin para vídeos
    list_display = ('nome_video', 'ano_publicacao', 'colecao', 'qtvideos', 'estante', 'data_cadastro', 'get_nome_escola')
    search_fields = ('nome_video', 'colecao')
    list_filter = ('nome_video',)
    ordering = ('nome_video',)

    # Exibir o nome da escola no list_display
    def get_nome_escola(self, obj):
        return obj.escola.nome_escola if obj.escola else 'Escola não definida'
    get_nome_escola.short_description = 'Nome da Escola'

    # Definir o queryset com base no usuário logado
    # Definir o queryset com base no usuário logado
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusuários veem todos os registros
        if request.user.is_superuser:
            return qs

        # Usuários que não são superusuários visualizam apenas os livros da escola associada
        if request.user.escola:
            return qs.filter(escola=request.user.escola)

        # Se o usuário não tiver uma escola associada, retorna nenhum registro
        return qs.none()

    # Definir permissões de edição
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

    # Salvar o modelo com a escola associada ao usuário
    def save_model(self, request, obj, form, change):
        # Se o usuário não for superusuário, atribuir automaticamente a escola
        if not request.user.is_superuser:
            obj.escola = request.user.escola
        super().save_model(request, obj, form, change)

    # Definir permissões de edição para o grupo "Alunos"
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_change_permission(request, obj)

    # Bloquear permissão de adição para o grupo "Alunos"
    def has_add_permission(self, request):
        if request.user.groups.filter(name='Alunos').exists():
            return False
        return super().has_add_permission(request)

    # Ocultar o menu "Escola" para não superusuários
    def has_module_permission(self, request):
        # Apenas superusuário deve ver o menu
        return request.user.is_superuser

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
    list_display = ('nome_cliente', 'email', 'situacao', 'serie', 'nr_telefone', 'tipo_usuario', 'cpf', 'get_nome_escola')
    search_fields = ('nome_cliente', 'email', 'situacao', 'serie', 'nr_telefone', 'tipo_usuario', 'cpf', 'escola__nome_escola')
    ordering = ('nome_cliente',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and request.user.groups.filter(name='Gerentes').exists():
            if 'escola' in form.base_fields:
                form.base_fields['escola'].disabled = True
                form.base_fields['escola'].initial = request.user.escola
        return form

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola
    get_nome_escola.short_description = 'Nome da Escola'

    def has_module_permission(self, request):
        """Permite que Gerentes vejam os clientes no menu."""
        return request.user.is_superuser or request.user.groups.filter(name='Gerentes').exists()

    def has_add_permission(self, request):
        """Impede que Gerentes adicionem novos clientes."""
        return request.user.is_superuser  # Apenas superusuários podem adicionar

    def has_change_permission(self, request, obj=None):
        """Permite que Gerentes editem clientes."""
        return request.user.is_superuser or request.user.groups.filter(name='Gerentes').exists()

    def has_delete_permission(self, request, obj=None):
        """Permite que Gerentes excluam clientes."""
        return request.user.is_superuser or request.user.groups.filter(name='Gerentes').exists()

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

class EmprestimoLivroAdmin(admin.ModelAdmin):
    list_display = (
    'get_titulo', 'get_nome_cliente', 'get_qtlivros', 'data_emprestimo', 'data_devolucao', 'multa', 'escola')
    fields = ('titulo', 'nome_cliente', 'data_emprestimo', 'data_devolucao', 'multa', 'escola')  # ❌ Removemos 'get_qtlivros'
    list_filter = ('data_emprestimo', 'data_devolucao')
    ordering = ('data_emprestimo',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Gerentes').exists():
            return qs.filter(escola=request.user.escola)
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        # NÃO adiciona 'request' ao kwargs
        form = super().get_form(request, obj, **kwargs)  # Chama o método da superclasse corretamente
        if not request.user.is_superuser and request.user.groups.filter(name='Gerentes').exists():
            if 'escola' in form.base_fields:
                form.base_fields['escola'].disabled = True
                form.base_fields['escola'].initial = request.user.escola
        return form

    def save_model(self, request, obj, form, change):
        """Garante que a escola salva seja sempre a do usuário logado."""
        if not request.user.is_superuser:
            obj.escola = request.user.escola  # Define a escola do usuário logado
        super().save_model(request, obj, form, change)

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

    def has_module_permission(self, request):
        """Define se o menu do módulo será visível no Django Admin."""
        return request.user.is_superuser  # Apenas superusuário vê o menu

class EmprestimoVideoAdmin(BaseEscolaAdmin):
    list_display = ('get_nome_video', 'get_nome_cliente', 'get_qtvideos', 'data_emprestimo', 'data_devolucao', 'multa', 'escola')
    list_filter = ('data_emprestimo', 'data_devolucao')
    fields = ('nome_video', 'nome_cliente', 'data_emprestimo', 'data_devolucao', 'multa','escola')  # Garante que o campo aparece no Django Admin
    ordering = ('data_emprestimo',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Gerentes').exists():
            return qs.filter(escola=request.user.escola)
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        # NÃO adiciona 'request' ao kwargs
        form = super().get_form(request, obj, **kwargs)  # Chama o método da superclasse corretamente
        if not request.user.is_superuser and request.user.groups.filter(name='Gerentes').exists():
            if 'escola' in form.base_fields:
                form.base_fields['escola'].disabled = True
                form.base_fields['escola'].initial = request.user.escola
        return form

    def get_nome_video(self, obj):
        return obj.nome_video.nome_video

    get_nome_video.short_description = 'Nome do Video'

    def get_nome_cliente(self, obj):
        return obj.nome_cliente.nome_cliente

    get_nome_cliente.short_description = 'Nome do Cliente'

    def get_qtvideos(self, obj):
        return obj.nome_video.qtvideos

    get_qtvideos.short_description = 'Qtdes de Videos'

    def get_nome_escola(self, obj):
        return obj.escola.nome_escola

    get_nome_escola.short_description = 'Nome da Escola'

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

