from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render, get_object_or_404
<<<<<<< HEAD
<<<<<<< HEAD
from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages  # Importa o sistema de mensagens do Django
from .models import CustomUser
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login

from .forms import (
    ClienteForm, EventosForm, EmprestimoLivroForm, EmprestimoVideoForm, AutoresForm, EditorasForm,
    VideosForm, ReservasForm, EscolaForm, LivroForm
)

=======
from django.shortcuts import redirect
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
from django.shortcuts import redirect
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
from .models import (
    Autores, Editoras, Generos, Eventos, Assuntos, Livros, Escola, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)

<<<<<<< HEAD
<<<<<<< HEAD
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redireciona para o Dashboard
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "registration/login.html")

def home_view(request):
    return render(request, "gestao/home.html")  # Garante que a home seja carregada corretamente

def success(request):
    return render(request, 'success.html', {'message': 'Cadastro realizado com sucesso!'})

@login_required
def base_site(request):
    return render(request, 'admin/base_site.html')  # Verifique o caminho correto do template

@login_required
def dashboard_view(request):
    # Obtém a escola do usuário logado
    escola_usuario = request.user.escola

    # Filtra os dados de acordo com a escola
    total_livros = Livros.objects.filter(escola=escola_usuario).count()
    total_alunos = Clientes.objects.filter(escola=escola_usuario).count()

    # Calcula os livros emprestados (empréstimos sem data_devolucao, mas com data_emprestimo registrada)
    livros_emprestados = EmprestimoLivro.objects.filter(
        escola=escola_usuario,
        data_devolucao__isnull=True,  # Apenas onde a devolução não foi registrada
        data_emprestimo__isnull=False  # Garante que há uma data de empréstimo
    ).count()

    # Envia os dados para o template
    context = {
        'total_livros': total_livros,
        'total_alunos': total_alunos,
        'livros_emprestados': livros_emprestados,  # Agora mostra a contagem correta de livros emprestados
    }

    return render(request, "gestao/dashboard.html", context)

class VideoDetailView(DetailView):
    model = Videos
    template_name = 'videos/detalhe_video.html'  # Nome do template que será usado
    context_object_name = 'video'  # Nome usado no template

def excluir_reserva(request):
    if request.method == "POST":
        reserva_id = request.POST.get("reserva_id")  # Obtém o ID do formulário
        reserva = get_object_or_404(Reservas, reserva_id=reserva_id)
        reserva.delete()
        return redirect("cadastro_reservas")  # Redireciona após excluir

    reservas = Reservas.objects.all()  # Lista todas as reservas para exclusão
    return render(request, "excluir_reserva.html", {"reservas": reservas})

def localizar_reserva(request):
    # Lógica para buscar uma reserva pelo ID ou Nome do Cliente
    query = request.GET.get("q")
    reservas = Reservas.objects.filter(nome_cliente__nome_cliente__icontains=query) if query else []
    return render(request, "localizar_reserva.html", {"reservas": reservas, "query": query})

def cadastro_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)  # ✅ Remova request=request
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('cadastro_cliente')
    else:
        form = ClienteForm()  # ✅ Remova request=request

    return render(request, 'gestao/cadastro_cliente.html', {'form': form})

def cadastro_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Escola cadastrada com sucesso!")
            return redirect('cadastro_escola')  # Redireciona para limpar o formulário
        else:
            messages.error(request, "Erro ao cadastrar a escola. Verifique os campos.")

    else:
        form = EscolaForm()

    return render(request, 'gestao/cadastro_escola.html', {'form': form})

def emprestimo_livro(request):
    """View para cadastro de empréstimo de vídeos"""

    if not request.user.is_authenticated:
        return redirect('login')

    # Obtém a escola do usuário logado
    escola_usuario = getattr(request.user, 'escola', None)

    # Filtra os livros apenas da escola do usuário logado
    livros = Livros.objects.filter(escola=escola_usuario) if escola_usuario else Livros.objects.none()

    if request.method == 'POST':
        form = EmprestimoLivroForm(request.POST, request=request)  # ✅ Passando request corretamente
        if form.is_valid():
            emprestimo = form.save(commit=False)

            if not escola_usuario:
                messages.error(request, "Erro: Usuário não tem uma escola associada.")
                return redirect('emprestimolivro')

            # Define a escola corretamente antes de salvar
            emprestimo.escola = escola_usuario
            emprestimo.save()

            messages.success(request, "Empréstimo cadastrado com sucesso!")
            return redirect('emprestimolivro')
        else:
            # Mostra os erros do formulário na tela para depuração
            messages.error(request, f"Erro ao cadastrar empréstimo de livros. Verifique os campos. {form.errors}")
    else:
        form = EmprestimoLivroForm(request=request)  # ✅ Passando request corretamente
    return render(request, 'gestao/emprestimo_livro.html', {'form': form})

def emprestimo_video(request):
    if request.method == "POST":
        form = EmprestimoVideoForm(request.POST, user=request.user)  # Passa o usuário
        if form.is_valid():
            emprestimo = form.save(commit=False)
            if not request.user.is_superuser:
                emprestimo.escola_id = request.user.escola.escola_id
            emprestimo.save()
            messages.success(request, "Empréstimo cadastrado com sucesso!")
            return redirect("emprestimo_video")
        else:
            messages.error(request, "Erro ao cadastrar empréstimo de vídeos. Verifique os campos.")
    else:
        form = EmprestimoVideoForm(user=request.user)  # Passa o usuário para o form

    return render(request, "gestao/emprestimo_video.html", {"form": form})

def cadastro_reservas(request):
    if request.method == "POST":
        form = ReservasForm(request.POST)

        # ✅ Verifica se o usuário tem uma escola associada antes de salvar
        if not request.user.is_superuser:
            if hasattr(request.user, 'escola') and isinstance(request.user.escola, Escola):
                escola = request.user.escola
                request.POST = request.POST.copy()
                request.POST['escola'] = escola.pk  # ✅ Define a escola explicitamente
            else:
                messages.error(request, "Erro ao identificar a escola do usuário. Certifique-se de que o usuário está associado a uma escola.")
                return redirect('cadastro_reservas')

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.escola = request.user.escola  # ✅ Assegura que a escola seja atribuída corretamente
            reserva.save()
            messages.success(request, "Reserva cadastrada com sucesso!")
            return redirect('cadastro_reservas')
        else:
            messages.error(request, "Erro ao cadastrar a reserva. Verifique os campos abaixo.")
            print(form.errors)  # Debug no terminal para identificar erros

    else:
        form = ReservasForm()

    reservas = Reservas.objects.all()
    return render(request, 'gestao/cadastro_reservas.html', {'form': form, 'reservas': reservas})

def alterar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reservas, pk=reserva_id)

    # Formatação correta das datas para exibição no formulário
    if reserva.data_reserva:
        reserva.data_reserva = reserva.data_reserva.strftime('%Y-%m-%d')
    if reserva.data_retirada:
        reserva.data_retirada = reserva.data_retirada.strftime('%Y-%m-%d')
    if reserva.data_devolucao:
        reserva.data_devolucao = reserva.data_devolucao.strftime('%Y-%m-%d')

    if request.method == "POST":
        form = ReservasForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva alterada com sucesso!")
            return redirect('cadastro_reservas')
    else:
        form = ReservasForm(instance=reserva)

    return render(request, 'alterar_reserva.html', {'form': form})

def cadastro_eventos(request):
    if request.method == "POST":
        form = EventosForm(request.POST, request=request)  # Passa o request
        if form.is_valid():
            evento = form.save(commit=False)  # Não salva ainda
            if not request.user.is_superuser:
                evento.escola = request.user.escola  # Atribui a escola automaticamente para Gerentes
            evento.save()
            messages.success(request, "✅ Evento cadastrado com sucesso!")
            return redirect('cadastro_eventos')  # Redireciona para a mesma página
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = EventosForm()  # Passa o request

    eventos = Eventos.objects.all()  # Obtém todos os eventos cadastrados

    return render(request, 'gestao/cadastro_eventos.html', {'form': form, 'eventos': eventos})

def excluir_evento(request):
    if request.method == "POST":
        evento_id = request.POST.get("evento_id")

        if not evento_id:
            messages.error(request, "Selecione um evento para excluir.")
            return redirect("excluir_evento")

        try:
            evento = get_object_or_404(Eventos, pk=int(evento_id))
            evento.delete()
            messages.success(request, "Evento excluído com sucesso!")
        except ValueError:
            messages.error(request, "Erro ao excluir o evento. Selecione um evento válido.")

        return redirect("excluir_evento")

    eventos = Eventos.objects.all()
    return render(request, "excluir_evento.html", {"eventos": eventos})

def alterar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, evento_id=evento_id)

    if request.method == 'POST':
        form = EventosForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('gestao/cadastro_eventos')
    else:
        form = EventosForm(instance=evento)

    return render(request, 'alterar_evento.html', {'form': form, 'evento': evento})

def lista_eventos(request):
    eventos = Eventos.objects.all()  # Pegando todos os eventos
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

class ListaEventosView(ListView):
    model = Eventos
    template_name = 'eventos/lista_eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        escola_do_usuario = self.request.user.escola  # Obtém a escola do usuário logado
        return Eventos.objects.filter(escola=escola_do_usuario)  # Filtra apenas os eventos da escola do usuário

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['high_contrast'] = self.request.session.get('high_contrast', False)  # Modo de alto contraste
        return context

@login_required
def cadastro_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request=request)  # ✅ Passando request corretamente
        if form.is_valid():
            form.save()
            return redirect('cadastro-livro')  # ✅ Redireciona após o cadastro
    else:
        form = AutorForm(request=request)  # ✅ Passando request corretamente

    return render(request, 'gestao/cadastro_autor.html', {'form': form})

@login_required
def cadastro_editora(request):
    if request.method == "POST":
        form = EditoraForm(request.POST)
        if form.is_valid():
            editora = form.save(commit=False)
            editora.escola = request.user.escola  # Define automaticamente a escola do usuário
            editora.save()
            return redirect('cadastro_editora')  # Atualiza a página após salvar
    else:
        form = EditoraForm(initial={'escola': request.user.escola})  # Define a escola automaticamente

    return render(request, 'gestao/cadastro_editora.html', {'form': form})

def cadastro_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request=request)
        if form.is_valid():
            livro = form.save(commit=False)
            if not livro.escola:
                livro.escola = request.customuser.escola  # ✅ Garante que a escola seja atribuída
            livro.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect('cadastro_livro')  # ✅ Garante que o nome está correto
        else:
            messages.error(request, "Erro ao cadastrar o livro. Verifique os campos.")
    else:
        form = LivroForm(request=request)

    return render(request, 'gestao/cadastro_livro.html', {'form': form})

def cadastro_video(request):
    if request.method == "POST":
        form = VideosForm(request.POST, request=request)
        if form.is_valid():
            video = form.save(commit=False)
            if not request.user.is_superuser:  # 🔥 Garante que Gerentes sempre salvem com a escola correta
                video.escola = request.user.escola
            video.save()
            messages.success(request, "🎉 Vídeo cadastrado com sucesso!")
            return redirect('cadastro_video')
    else:
        form = VideosForm(request=request)

    return render(request, 'gestao/cadastro_video.html', {'form': form})

class EscolaCreateView(CreateView):
    model = Escola
    form_class = EscolaForm
    template_name = 'cadastro_cliente.html'
    success_url = '/cliente/'  # URL para redirecionamento após cadastro bem-sucedido
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

# Função para alternar o modo de alto contraste e salvar na sessão
def toggle_contrast(request):
    # Alterna o estado do modo de alto contraste na sessão
    current_contrast = request.session.get('high_contrast', False)
    request.session['high_contrast'] = not current_contrast
    return redirect('home')

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
def home(request):
    # Passa o estado de alto contraste para o template
    high_contrast = request.session.get('high_contrast', False)

    if request.user.is_authenticated:
        return redirect('/admin/')
    else:
        return render(request, 'gestao/home.html', {'high_contrast': high_contrast})

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # Adicione o usuário ao grupo após a criação
            group = Group.objects.get(name='Gerentes')  # Nome do grupo
            user.groups.add(group)  # Adiciona o usuário ao grupo

            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()

    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'signup.html', {'form': form, 'high_contrast': high_contrast})

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
def sua_visualizacao(request):
    from .forms import SeuFormulario

    if request.method == 'POST':
        form = SeuFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SeuFormulario()

    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'login.html', {'form': form, 'high_contrast': high_contrast})

<<<<<<< HEAD
<<<<<<< HEAD
def minha_view(request):
    """
    View para cadastro de livros, garantindo acessibilidade e exibição de erros.
    """

    # Ativa as chaves estrangeiras no SQLite (se necessário)
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = ON;")

=======

def minha_view(request):
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

def minha_view(request):
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
    if request.method == 'POST':
        form = LivrosForm(request.POST)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
<<<<<<< HEAD
            return redirect('success')  # Certifique-se de que 'success' está configurado em urls.py
        else:
            # ✅ Exibir mensagens de erro no template
            print(form.errors)  # Apenas para debug no console
=======
            return redirect('success')
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
            return redirect('success')
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
    else:
        form = LivrosForm()

    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
<<<<<<< HEAD
<<<<<<< HEAD

    return render(request, 'template.html', {
        'livros_form': form,
        'high_contrast': high_contrast
    })
=======
    return render(request, 'template.html', {'livros_form': form, 'high_contrast': high_contrast})

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
    return render(request, 'template.html', {'livros_form': form, 'high_contrast': high_contrast})

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class ListaLivrosView(ListView):
    model = Livros
    template_name = 'livros/lista_livros.html'
    context_object_name = 'livros'

    def get_queryset(self):
<<<<<<< HEAD
<<<<<<< HEAD
        """Filtra os livros pela escola do usuário logado"""
        if self.request.user.is_authenticated:
            return Livros.objects.filter(escola=self.request.user.escola)
        return Livros.objects.none()
=======
        escola_do_usuario = self.request.user.escola  # Atribui a escola do usuário logado
        return Livros.objects.filter(escola=escola_do_usuario)
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
        escola_do_usuario = self.request.user.escola  # Atribui a escola do usuário logado
        return Livros.objects.filter(escola=escola_do_usuario)
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['high_contrast'] = self.request.session.get('high_contrast', False)  # Passa o modo de alto contraste
        return context

class ListaVideosView(ListView):
    model = Videos
    template_name = 'videos/lista_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        # Supondo que o usuário logado tenha uma relação com a escola
        escola_do_usuario = self.request.user.escola
        return Videos.objects.filter(escola=escola_do_usuario)

def lista_autores(request):
    escola_do_usuario = request.user.userprofile.escola  # Acessa a escola através do perfil do usuário
    autores = Autores.objects.filter(escola=escola_do_usuario)
    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'autores/lista_autores.html', {'autores': autores, 'high_contrast': high_contrast})

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
def selecionar_escola(request):
    if not request.user.is_authenticated:
        return redirect('login')

    escola_do_usuario = getattr(request.user, 'escola', None)  # ou request.user.userprofile.escola se usar UserProfile
    if escola_do_usuario:
        request.session['escola_id'] = escola_do_usuario.id
        return redirect('dashboard')

    if request.method == 'POST':
        escola_id = request.POST.get('escola_id')
        escola = get_object_or_404(Escola, id=escola_id)
        request.session['escola_id'] = escola.id
        return redirect('dashboard')

    escolas = Escola.objects.all()
    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'selecionar_escola.html', {'escolas': escolas, 'high_contrast': high_contrast})

@login_required
def dashboard(request):
    escola_id = request.session.get('escola_id')
    if escola_id:
        escola_selecionada = Escola.objects.get(id=escola_id)
        emprestimos = EmprestimoVideo.objects.filter(escola=escola_selecionada)
    else:
        emprestimos = EmprestimoVideo.objects.none()

    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'dashboard.html', {'emprestimos': emprestimos, 'high_contrast': high_contrast})

<<<<<<< HEAD
<<<<<<< HEAD



=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
def toggle_contrast(request):
    # Alterna o estado de alto contraste na sessão
    current_contrast = request.session.get('high_contrast', False)
    request.session['high_contrast'] = not current_contrast
    return redirect('home')  # Redireciona para a página inicial
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083


