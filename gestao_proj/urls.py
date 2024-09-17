from django.contrib import admin
from django.urls import path, include
from gestao.views import home, signup  # Importe as funções home e signup do módulo todos.views
from django.contrib.auth.views import LogoutView  # Importe a view de logout padrão do Django
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticação padrão do Django
    path('signup/', signup, name='signup'),  # Use a função signup diretamente
    path('', home),
    path('logout/', LogoutView.as_view(), name='logout'),  # Configuração da rota de logout
]

# Adicione esta linha para incluir as URLs de autenticação e signup
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', include('gestao.urls')),  # Assumindo que você tem uma URL para a página de signup
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



