from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # Importa o seu modelo de usuário personalizado
import requests

from .models import (
    Autores, Editoras, Generos, Assuntos, Eventos, Livros, Escola, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)

class AutoresForm(forms.ModelForm):
    class Meta:
        model = Autores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o request foi passado e se o usuário não é superusuário
        if request and not request.user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = request.user.escola  # Obtém a escola associada ao usuário
            self.fields['escola'].queryset = Escola.objects.filter(id=escola.id)  # Filtra a escola do usuário
            self.fields['escola'].initial = escola  # Define a escola inicial
            self.fields['escola'].disabled = True  # Desabilita o campo

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livros
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o usuário é superusuário
        if not user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = user.escola  # Aqui você obtém a escola associada ao usuário
            self.fields['escola'].queryset = escola
            self.fields['escola'].initial = escola
            self.fields['escola'].disabled = True  # Desabilita o campo

class VideosForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o usuário é superusuário
        if not user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = user.escola  # Aqui você obtém a escola associada ao usuário
            self.fields['escola'].queryset = escola
            self.fields['escola'].initial = escola
            self.fields['escola'].disabled = True  # Desabilita o campo

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o request foi passado e se o usuário não é superusuário
        if request and not request.user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = request.user.escola  # Obtém a escola associada ao usuário
            self.fields['escola'].queryset = Escola.objects.filter(id=escola.id)  # Filtra a escola do usuário
            self.fields['escola'].initial = escola  # Define a escola inicial
            self.fields['escola'].disabled = True  # Desabilita o campo

class ReservasForm(forms.ModelForm):
    class Meta:
        model = Reservas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o request foi passado e se o usuário não é superusuário
        if request and not request.user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = request.user.escola  # Obtém a escola associada ao usuário
            self.fields['escola'].queryset = Escola.objects.filter(id=escola.id)  # Filtra a escola do usuário
            self.fields['escola'].initial = escola  # Define a escola inicial
            self.fields['escola'].disabled = True  # Desabilita o campo

class EmprestimoLivroForm(forms.ModelForm):
    class Meta:
        model = EmprestimoLivro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o request foi passado e se o usuário não é superusuário
        if request and not request.user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = request.user.escola  # Obtém a escola associada ao usuário
            self.fields['escola'].queryset = Escola.objects.filter(id=escola.id)  # Filtra a escola do usuário
            self.fields['escola'].initial = escola  # Define a escola inicial
            self.fields['escola'].disabled = True  # Desabilita o campo

class EmprestimoVideoForm(forms.ModelForm):
    class Meta:
        model = EmprestimoVideo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Recebe o request
        super().__init__(*args, **kwargs)

        # Verifica se o request foi passado e se o usuário não é superusuário
        if request and not request.user.is_superuser:
            # Para não superusuários, o campo escola é fixo e não editável
            escola = request.user.escola  # Obtém a escola associada ao usuário
            self.fields['escola'].queryset = Escola.objects.filter(id=escola.id)  # Filtra a escola do usuário
            self.fields['escola'].initial = escola  # Define a escola inicial
            self.fields['escola'].disabled = True  # Desabilita o campo

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'

# Formulário para alteração de usuários existentes
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User  # Use o modelo personalizado
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'escola']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use o modelo personalizado
        fields = ['username', 'email', 'escola', 'is_superuser']  # Adicione 'is_superuser' aqui se necessário

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está sendo usado.")
        return email

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'escola']
