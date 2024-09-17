from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include
from gestao.views import home, signup  # Importe as funções home e signup do módulo todos.views
from django.contrib.auth.views import LogoutView  # Importe a view de logout padrão do Django
from django.conf import settings
from django.conf.urls.static import static
from gestao import views  # Importe o views que contém lista_autores
from .views import home, toggle_contrast
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)









