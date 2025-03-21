from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include
from gestao.views import home, signup  # Importe as funções home e signup do módulo todos.views
from django.contrib.auth.views import LogoutView  # Importe a view de logout padrão do Django
from django.conf import settings
from django.conf.urls.static import static
from gestao import views  # Importe o views que contém lista_autores
from .views import home, toggle_contrast
<<<<<<< HEAD
from .views import ListaVideosView, ListaLivrosView, ListaEventosView
from django.views.generic import TemplateView  # Adicione esta linha
from django.db import connection
from .views import excluir_reserva, localizar_reserva, alterar_reserva # Importe as views
from .views import excluir_evento, alterar_evento # Importe as vie
from .views import base_site  # ✅ Importa a view corretamente
from .views import success
from .views import dashboard_view  # Importe a view corretamente
from .views import VideoDetailView  # Certifique-se de importar corretamente
from .views import home_view, login_view, dashboard_view  # Certifique-se de importar a view correta

from .views import (
    home, EscolaCreateView, cadastro_escola, cadastro_livro, cadastro_video, cadastro_reservas,
    cadastro_eventos, emprestimo_livro, emprestimo_video, cadastro_cliente, cadastro_autor, cadastro_editora,
    ListaVideosView, ListaLivrosView, ListaEventosView, excluir_reserva, localizar_reserva, alterar_reserva,
    excluir_evento, alterar_evento, base_site, success
)

urlpatterns = [
    path("", home_view, name="home"),  # Tela inicial redirecionando para login
    path("login/", login_view, name="login"),  # Tela de login (login.html)
    path("logout/", LogoutView.as_view(), name="logout"),  # URL para logout
    path('signup/', signup, name='signup'),  # Outras rotas do seu aplicativo...
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclui URLs de autenticação padrão
    path('accounts/login/', LoginView.as_view(), name='login'),  # Definição explícita da URL de login
    path('toggle-contrast/', toggle_contrast, name='toggle_contrast'),  # A URL para alternar o contraste

    # Cadastro
    path('cadastro-escola/', cadastro_escola, name='cadastro_escola'),
    path('cadastro-livro/', cadastro_livro, name='cadastro_livro'),
    path('cadastro-video/', cadastro_video, name='cadastro_video'),
    path('cadastro-reservas/', cadastro_reservas, name='cadastro_reservas'),
    path('cadastro-cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('cadastro-eventos/', cadastro_eventos, name='cadastro_eventos'),
    path('cadastro-autor/', cadastro_autor, name='cadastro_autor'),
    path('cadastro-editora/', cadastro_editora, name='cadastro_editora'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # Emprestimos
    path('emprestimolivro/', views.emprestimo_livro, name='emprestimolivro'),
    path("emprestimo-video/", emprestimo_video, name="emprestimo_video"),

    # Reservas
    path('livros/', ListaLivrosView.as_view(), name='lista_livros'),
    path('excluir-reserva/', excluir_reserva, name='excluir_reserva'),
    path('localizar-reserva/', localizar_reserva, name='localizar_reserva'),
    path("alterar-reserva/<int:reserva_id>/", alterar_reserva, name="alterar_reserva"),

    # Eventos
    path("eventos/", ListaEventosView.as_view(), name="lista_eventos"),
    path('lista-eventos-fbv/', views.lista_eventos, name='lista_eventos_fbv'),
    path('excluir-evento/', excluir_evento, name='excluir_evento'),
    path('alterar-evento/<int:evento_id>/', alterar_evento, name='alterar_evento'),

    # Outros
    path('base_site/', base_site, name='base_site'),
    path('success/', success, name='success'),
    path('videos/', ListaVideosView.as_view(), name='lista_videos'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    # Gráficos
    path('livros/cadastro/', views.cadastro_livro, name='cadastro_livro'),
    path('videos/cadastro/', views.cadastro_video, name='cadastro_video'),
    path('alunos/cadastro/', views.cadastro_cliente, name='cadastro_cliente'),
    path('reservas/cadastro/', views.cadastro_reservas, name='cadastro_reservas'),
    path('eventos/cadastro/', views.cadastro_eventos, name='cadastro_eventos'),
    path('livros/emprestimo/', views.emprestimo_livro, name='emprestimo_livro'),
    path('videos/emprestimo/', views.emprestimo_video, name='emprestimo_video'),

=======
from .views import ListaVideosView
from .views import ListaLivrosView

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),  # Corrigido o caminho da página de login
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),    # Outras rotas do seu aplicativo...
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclui URLs de autenticação padrão
    path('accounts/login/', LoginView.as_view(), name='login'),  # Definição explícita da URL de login
    path('autores/', views.lista_autores, name='lista_autores'),  # A função lista_autores agora será reconhecida
    path('livros/', ListaLivrosView.as_view(), name='lista_livros'),
    path('videos/', ListaVideosView.as_view(), name='lista_videos'),
    path('toggle-contrast/', toggle_contrast, name='toggle_contrast'),  # A URL para alternar o contraste
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
<<<<<<< HEAD
    path('dashboard/', views.dashboard, name='dashboard'),


















=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083









