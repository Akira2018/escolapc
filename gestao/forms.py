from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  # Importa o seu modelo de usuário personalizado
import requests
<<<<<<< HEAD
<<<<<<< HEAD
from django.urls import reverse
from django.utils.safestring import mark_safe
from gestao.models import CustomUser  # Certifique-se de importar seu modelo personalizado
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

from .models import (
    Autores, Editoras, Generos, Assuntos, Eventos, Livros, Escola, Videos,
    Clientes, Reservas, EmprestimoLivro, EmprestimoVideo
)

<<<<<<< HEAD
<<<<<<< HEAD
class EventosForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['nome_evento', 'data_evento', 'local', 'escola']
        widgets = {
            'nome_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'data_evento': forms.DateInput(
                format='%d/%m/%Y',  # Formato brasileiro
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            usuario = self.request.user  # Pega o usuário logado

            # 🚨 Verifica se o usuário tem uma escola associada antes de acessar .escola_id
            if hasattr(usuario, 'escola_id') and usuario.escola_id:
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=usuario.escola_id)
                self.fields['escola'].initial = usuario.escola
                self.fields['escola'].widget.attrs['readonly'] = True
            else:
                # 🚨 Se não houver escola associada, evitar erro e exibir um aviso
                self.fields['escola'].queryset = Escola.objects.none()
                self.fields['escola'].initial = None
                raise forms.ValidationError("⚠️ O usuário não tem uma escola associada. Contate o administrador.")

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome_cliente', 'email', 'situacao', 'serie', 'tipo_usuario', 'cpf',
            'nr_telefone', 'cep', 'logradouro', 'bairro', 'cidade', 'estado',
            'nr_imovel', 'observacao', 'escola'
        ]
        widgets = {
            'nome_cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Aluno'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'situacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Situação do Aluno'}),
            'serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serie do Aluno'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'nr_telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do Telefone'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'nr_imovel': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            request = kwargs.pop('request', None)  # ✅ Remove 'request' de kwargs antes de chamar super()
            super().__init__(*args, **kwargs)  # ✅ Agora não há erro!

            if request:  # ✅ Apenas se request for passado
                usuario = request.user
                if usuario.is_superuser:
                    self.fields['escola'].queryset = Escola.objects.all()
                else:
                    # ✅ Verifica se o usuário tem a escola definida corretamente
                    if hasattr(usuario, 'escola') and usuario.escola:
                        self.fields['escola'].queryset = Escola.objects.filter(id=usuario.escola.id)
                        self.fields['escola'].initial = usuario.escola
                    else:
                        self.fields['escola'].queryset = Escola.objects.none()

                    self.fields['escola'].widget.attrs['readonly'] = True

class AutoresForm(forms.ModelForm):
    class Meta:
        model = Autores
        fields = ['nome_autor', 'nacionalidade', 'biografia', 'escola']
        widgets = {
            'nome_autor': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pega o request se existir
        super().__init__(*args, **kwargs)

        # Obtém a escola associada ao CustomUser
        escola_usuario = None
        if self.request and isinstance(self.request.user, CustomUser):
            escola_usuario = self.request.user.escola  # Pega corretamente a escola do CustomUser

        if self.request and self.request.user.is_superuser:
            # Superusuário pode ver todas as escolas
            self.fields['escola'].queryset = Escola.objects.all()
        else:
            if escola_usuario and isinstance(escola_usuario, Escola):
                # Usuário normal vê apenas a própria escola
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=escola_usuario.escola_id)
                self.fields['escola'].initial = escola_usuario
                self.fields['escola'].widget.attrs['readonly'] = True  # Impede edição
            else:
                self.fields['escola'].queryset = Escola.objects.none()  # Se não houver escola válida
                self.fields['escola'].initial = None
                self.fields['escola'].widget.attrs['disabled'] = True  # Impede seleção manual

class EditorasForm(forms.ModelForm):
    class Meta:
        model = Editoras
        fields = ['nome_editora', 'pais', 'escola']
        widgets = {
            'nome_editora': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
             'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pega o request se existir
        super().__init__(*args, **kwargs)

        # Obtém a escola associada ao CustomUser
        escola_usuario = None
        if self.request and isinstance(self.request.user, CustomUser):
            escola_usuario = self.request.user.escola  # Pega corretamente a escola do CustomUser

        if self.request and self.request.user.is_superuser:
            # Superusuário pode ver todas as escolas
            self.fields['escola'].queryset = Escola.objects.all()
        else:
            if escola_usuario and isinstance(escola_usuario, Escola):
                # Usuário normal vê apenas a própria escola
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=escola_usuario.escola_id)
                self.fields['escola'].initial = escola_usuario
                self.fields['escola'].widget.attrs['readonly'] = True  # Impede edição
            else:
                self.fields['escola'].queryset = Escola.objects.none()  # Se não houver escola válida
                self.fields['escola'].initial = None
                self.fields['escola'].widget.attrs['disabled'] = True  # Impede seleção manual
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livros
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['titulo', 'nome_autor', 'nome_editora', 'isbn', 'ano_publicacao', 'qtlivros', 'localizacao', 'descricao', 'escola']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_autor': forms.Select(attrs={'class': 'form-control'}),
            'nome_editora': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'qtlivros': forms.NumberInput(attrs={'class': 'form-control'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pega o request se existir
        super().__init__(*args, **kwargs)

        # Obtém a escola associada ao CustomUser
        escola_usuario = None
        if self.request and isinstance(self.request.user, CustomUser):
            escola_usuario = self.request.user.escola  # Pega corretamente a escola do CustomUser

        if self.request and self.request.user.is_superuser:
            # Superusuário pode ver todas as escolas
            self.fields['escola'].queryset = Escola.objects.all()
        else:
            if escola_usuario and isinstance(escola_usuario, Escola):
                # Usuário normal vê apenas a própria escola
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=escola_usuario.escola_id)
                self.fields['escola'].initial = escola_usuario
                self.fields['escola'].widget.attrs['readonly'] = True  # Impede edição
            else:
                self.fields['escola'].queryset = Escola.objects.none()  # Se não houver escola válida
                self.fields['escola'].initial = None
                self.fields['escola'].widget.attrs['disabled'] = True  # Impede seleção manual
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class VideosForm(forms.ModelForm):
    class Meta:
        model = Videos
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['nome_video', 'ano_publicacao', 'colecao', 'qtvideos', 'estante', 'observacao', 'data_cadastro', 'escola']
        widgets = {
            'nome_video': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'colecao': forms.TextInput(attrs={'class': 'form-control'}),
            'qtvideos': forms.NumberInput(attrs={'class': 'form-control'}),
            'estante': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_cadastro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            usuario = self.request.user
            if usuario.is_superuser:
                self.fields['escola'].queryset = Escola.objects.all()
            else:
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=usuario.escola.escola_id)
                self.fields['escola'].initial = usuario.escola
                self.fields['escola'].widget = forms.HiddenInput()
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class ReservasForm(forms.ModelForm):
    class Meta:
        model = Reservas
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['titulo', 'nome_cliente', 'data_reserva', 'data_retirada', 'data_devolucao', 'escola']
        widgets = {
            'titulo': forms.Select(attrs={'class': 'form-control'}),
            'nome_cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_reserva': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_retirada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)  # Captura o request
            super().__init__(*args, **kwargs)

            if self.request:
                usuario = self.request.user
                if not usuario.is_superuser:
                    # ✅ Filtra para garantir que a escola seja corretamente atribuída
                    self.fields['escola'].queryset = Escola.objects.filter(pk=usuario.escola.pk)
                    self.fields['escola'].initial = usuario.escola.pk  # Define a escola inicial correta
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class EmprestimoLivroForm(forms.ModelForm):
    class Meta:
        model = EmprestimoLivro
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['titulo', 'nome_cliente', 'data_emprestimo', 'data_devolucao', 'multa', 'escola']
        widgets = {
            'titulo': forms.Select(attrs={'class': 'form-control'}),
            'nome_cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_emprestimo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'multa': forms.NumberInput(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pega o request se existir
        super().__init__(*args, **kwargs)

        # Obtém a escola associada ao CustomUser
        escola_usuario = None
        if self.request and isinstance(self.request.user, CustomUser):
            escola_usuario = self.request.user.escola  # Pega corretamente a escola do CustomUser

        if self.request and self.request.user.is_superuser:
            # Superusuário pode ver todas as escolas
            self.fields['escola'].queryset = Escola.objects.all()
        else:
            if escola_usuario and isinstance(escola_usuario, Escola):
                # Usuário normal vê apenas a própria escola
                self.fields['escola'].queryset = Escola.objects.filter(escola_id=escola_usuario.escola_id)
                self.fields['escola'].initial = escola_usuario
                self.fields['escola'].widget.attrs['readonly'] = True  # Impede edição
            else:
                self.fields['escola'].queryset = Escola.objects.none()  # Se não houver escola válida
                self.fields['escola'].initial = None
                self.fields['escola'].widget.attrs['disabled'] = True  # Impede seleção manual

class EmprestimoVideoForm(forms.ModelForm):

    class Meta:
        model = EmprestimoVideo
        fields = ['nome_video', 'nome_cliente', 'data_emprestimo', 'data_devolucao', 'multa', 'escola']
        widgets = {
            'nome_video': forms.Select(attrs={'class': 'form-control'}),
            'nome_cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_emprestimo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'multa': forms.NumberInput(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o usuário da request
        super().__init__(*args, **kwargs)

        # Se o usuário não for superusuário, preencha automaticamente a escola
        if user and not user.is_superuser:
            if 'escola' in self.fields:
                self.fields['escola'].queryset = self.fields['escola'].queryset.filter(escola_id=user.escola_id)
                self.fields['escola'].initial = user.escola
                self.fields['escola'].widget.attrs['readonly'] = True  # Torna o campo somente leitura
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'
<<<<<<< HEAD
<<<<<<< HEAD
        widgets = {
            'nome_escola': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nr_telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'nr_imovel': forms.TextInput(attrs={'class': 'form-control'}),
            'erro_cep': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Obtém o request se for passado
        super().__init__(*args, **kwargs)

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if not cep:
            raise forms.ValidationError("O CEP é obrigatório.")
        return cep

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not "@" in email:
            raise forms.ValidationError("Digite um e-mail válido.")
        return email
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083

# Formulário para alteração de usuários existentes
class CustomUserChangeForm(UserChangeForm):
    class Meta:
<<<<<<< HEAD
<<<<<<< HEAD
        model = CustomUser  # Use o modelo personalizado
=======
        model = User  # Use o modelo personalizado
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
        model = User  # Use o modelo personalizado
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'escola']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
<<<<<<< HEAD
<<<<<<< HEAD
        model = CustomUser  # Use o modelo personalizado
=======
        model = User  # Use o modelo personalizado
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
        model = User  # Use o modelo personalizado
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
        fields = ['username', 'email', 'escola', 'is_superuser']  # Adicione 'is_superuser' aqui se necessário

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está sendo usado.")
        return email

class CustomUserForm(forms.ModelForm):
    class Meta:
<<<<<<< HEAD
<<<<<<< HEAD
        model = CustomUser
=======
        model = User
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
        model = User
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'escola']
