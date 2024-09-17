from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import redirect
from .models import (
    Autores, Editoras, Generos, Eventos, Assuntos, Livros, Escola, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)


# Função para alternar o modo de alto contraste e salvar na sessão
def toggle_contrast(request):
    # Alterna o estado do modo de alto contraste na sessão
    current_contrast = request.session.get('high_contrast', False)
    request.session['high_contrast'] = not current_contrast
    return redirect('home')


def home(request):
    # Passa o estado de alto contraste para o template
    high_contrast = request.session.get('high_contrast', False)

    if request.user.is_authenticated:
        return redirect('/admin/')
    else:
        return render(request, 'gestao/home.html', {'high_contrast': high_contrast})


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


def minha_view(request):
    if request.method == 'POST':
        form = LivrosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = LivrosForm()

    high_contrast = request.session.get('high_contrast', False)  # Inclui acessibilidade
    return render(request, 'template.html', {'livros_form': form, 'high_contrast': high_contrast})


class ListaLivrosView(ListView):
    model = Livros
    template_name = 'livros/lista_livros.html'
    context_object_name = 'livros'

    def get_queryset(self):
        escola_do_usuario = self.request.user.escola  # Atribui a escola do usuário logado
        return Livros.objects.filter(escola=escola_do_usuario)

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

def toggle_contrast(request):
    # Alterna o estado de alto contraste na sessão
    current_contrast = request.session.get('high_contrast', False)
    request.session['high_contrast'] = not current_contrast
    return redirect('home')  # Redireciona para a página inicial


