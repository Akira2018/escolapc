from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db import models  # Adicione essa linha
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render, get_object_or_404
from .models import (
    Autores, Editoras, Generos, Eventos, Assuntos, Livros, Escola, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)

def home(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    else:
        return render(request, 'gestao/home.html')


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
    return render(request, 'signup.html', {'form': form})

def sua_visualizacao(request):
    from .forms import SeuFormulario

    if request.method == 'POST':
        form = SeuFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SeuFormulario()

    return render(request, 'login.html', {'form': form})

def minha_view(request):
    if request.method == 'POST':
        form = LivrosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = LivrosForm()
    return render(request, 'template.html', {'livros_form': form})

class ListaLivrosView(ListView):
    model = Livros
    template_name = 'livros/lista_livros.html'
    context_object_name = 'livros'

    def get_queryset(self):
        # Supondo que o usuário logado tenha uma relação com a escola
        escola_do_usuario = self.request.user.escola  # Atribui a escola do usuário logado
        return Livros.objects.filter(escola=escola_do_usuario)  # Filtra os livros da escola do usuário

# Movendo a função lista_autores para fora da classe
def lista_autores(request):
    escola_do_usuario = request.user.userprofile.escola  # Acessa a escola através do perfil do usuário
    autores = Autores.objects.filter(escola=escola_do_usuario)
    return render(request, 'autores/lista_autores.html', {'autores': autores})

def selecionar_escola(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Verifica se o usuário já está associado a uma escola
    escola_do_usuario = getattr(request.user, 'escola', None)  # ou request.user.userprofile.escola se usar UserProfile
    if escola_do_usuario:
        request.session['escola_id'] = escola_do_usuario.id  # Armazena a escola na sessão
        return redirect('dashboard')

    # Se o usuário não estiver associado a uma escola, permite seleção manual
    if request.method == 'POST':
        escola_id = request.POST.get('escola_id')

        # Verifica se a escola selecionada existe
        escola = get_object_or_404(Escola, id=escola_id)

        # Armazena a escola na sessão
        request.session['escola_id'] = escola.id
        return redirect('dashboard')

    # Exibe todas as escolas para seleção, ou pode filtrar se necessário
    escolas = Escola.objects.all()
    return render(request, 'selecionar_escola.html', {'escolas': escolas})

@login_required
def dashboard(request):
    escola_id = request.session.get('escola_id')
    if escola_id:
        escola_selecionada = Escola.objects.get(id=escola_id)
        emprestimos = EmprestimoVideo.objects.filter(escola=escola_selecionada)
    else:
        emprestimos = EmprestimoVideo.objects.none()  # Não exibe nada se a escola não for selecionada
    return render(request, 'dashboard.html', {'emprestimos': emprestimos})

