from django.db import models
from django.db.models import PositiveIntegerField
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import requests
from django.contrib import messages
from django.db import transaction
from .utils import buscar_endereco_por_cep
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
import json
from validate_docbr import CPF
import time
from django.contrib.auth.models import User
from requests.exceptions import RequestException
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .models import User
# Obtendo o logger
logger = logging.getLogger(__name__)

# Ignorar o aviso
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Modelo Escola definido antes do modelo User
class Escola(models.Model):
    escola_id = models.AutoField(primary_key=True)
    nome_escola = models.CharField(max_length=100, verbose_name='Nome da Escola')
    email = models.EmailField(verbose_name='Digite o E-mail', blank=True)
    nr_telefone = models.CharField(max_length=30, unique=True, verbose_name='Número do Telefone')
    instituicao = models.CharField(max_length=100, blank=True, verbose_name='Instituição')
    cep = models.CharField(
        max_length=8,
        verbose_name='CEP do Imóvel',
        blank=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='CEP deve ter 8 dígitos')]
    )
    logradouro = models.CharField(max_length=100, verbose_name='Nome da Rua', blank=True)
    bairro = models.CharField(max_length=50, verbose_name='Bairro', blank=True)
    cidade = models.CharField(max_length=50, verbose_name='Cidade', blank=True)
    estado = models.CharField(max_length=2, verbose_name='Estado', blank=True)
    nr_imovel = models.CharField(max_length=10, verbose_name='Número do Imóvel', blank=True)
    observacao = models.TextField(max_length=100, blank=True, verbose_name='Observação')
    erro_cep = models.CharField(max_length=255, blank=True, verbose_name='Erro ao buscar o CEP')

    def __str__(self):
        return self.nome_escola

    def preencher_endereco_por_cep(self, request=None):
        try:
            self.cep = self.cep.strip().replace('-', '')
            url = f'https://viacep.com.br/ws/{self.cep}/json/'
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                self.logradouro = data.get('logradouro', '')
                self.bairro = data.get('bairro', '')
                self.cidade = data.get('localidade', '')
                self.estado = data.get('uf', '')

                if not all([self.logradouro, self.bairro, self.cidade, self.estado]):
                    self.erro_cep = 'CEP não encontrado ou dados incompletos.'
                    if request:
                        messages.error(request, self.erro_cep)
                else:
                    self.erro_cep = ''
            else:
                self.erro_cep = f"Erro na consulta do CEP: {response.status_code}"
                if request:
                    messages.error(request, self.erro_cep)

        except requests.exceptions.RequestException as e:
            self.erro_cep = f"Erro na requisição: {e}"
            if request:
                messages.error(request, self.erro_cep)

        if self.erro_cep:
            self.logradouro = ''
            self.bairro = ''
            self.cidade = ''
            self.estado = ''

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.preencher_endereco_por_cep(request)
        super().save(*args, **kwargs)

class Meta:
    db_table = 'gestao_escola'
    verbose_name = "Nome da Escola"
    verbose_name_plural = "Nome da Escola"

# Estendendo o modelo de usuário com AbstractUser
class User(AbstractUser):
    escola = models.ForeignKey('Escola', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'gestao_userprofile'  # Garanta que isso use uma tabela diferente
        ordering = ['escola']  # Ordena pelo campo 'escola' através da relação com 'user'

class Autores(models.Model):
    autor_id = models.AutoField(primary_key=True)
    nome_autor = models.CharField(max_length=100, unique=True, verbose_name='Nome do Autor')
    nacionalidade = models.CharField(max_length=50, verbose_name='Nacionalidade')
    biografia = models.TextField(blank=True, null=True, verbose_name='Biografia')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.nome_autor

    class Meta:
        ordering = ['nome_autor']
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

class Editoras(models.Model):
    editora_id = models.AutoField(primary_key=True)
    nome_editora = models.CharField(max_length=100, unique=True, verbose_name='Nome da Editora')
    pais = models.CharField(max_length=50, verbose_name='País')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.nome_editora

    class Meta:
        ordering = ['nome_editora']
        verbose_name = "Editora"
        verbose_name_plural = "Editoras"

class Generos(models.Model):
    genero_id = models.AutoField(primary_key=True)
    nome_genero = models.CharField(max_length=100, unique=True, verbose_name='Nome do Gênero')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.nome_genero

    class Meta:
        ordering = ['nome_genero']
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class Assuntos(models.Model):
    assunto_id = models.AutoField(primary_key=True)
    descr_assunto = models.CharField(max_length=100, unique=True, verbose_name='Nome do Assunto')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.descr_assunto

    class Meta:
        ordering = ['descr_assunto']
        verbose_name = "Assunto"
        verbose_name_plural = "Assuntos"

class Eventos(models.Model):
    evento_id = models.AutoField(primary_key=True)
    nome_evento = models.CharField(max_length=255)
    data_evento = models.DateTimeField()
    local = models.CharField(max_length=255)
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.nome_evento

    class Meta:
        ordering = ['nome_evento']
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

class Livros(models.Model):
    livro_id = models.AutoField(primary_key=True)  # Define a chave primária corretamente
    titulo = models.CharField(max_length=200, verbose_name='Título')
    nome_autor = models.ForeignKey(Autores, on_delete=models.CASCADE, verbose_name='Autor')
    nome_editora = models.ForeignKey(Editoras, on_delete=models.CASCADE, verbose_name='Editora', blank=True, null=True)
    nome_genero = models.ManyToManyField(Generos, verbose_name='Gêneros', blank=True)
    descr_assunto = models.ManyToManyField(Assuntos, verbose_name='Assuntos', blank=True)
    isbn = models.CharField(max_length=20, unique=True, verbose_name='ISBN', blank=True, null=True)
    edicao = models.CharField(max_length=50, verbose_name='Edição', blank=True, null=True)
    ano_publicacao = models.PositiveIntegerField(verbose_name='Ano de Publicação', blank=True, null=True)
    qtlivros = models.BigIntegerField(verbose_name='Quantidade de Livros', blank=True, null=True)
    localizacao = models.CharField(max_length=100, verbose_name='Localização', blank=True, null=True)
    descricao = models.TextField(blank=True, verbose_name='Descrição', null=True)
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['titulo']
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

class Videos(models.Model):
    video_id = models.AutoField(primary_key=True)
    nome_video = models.CharField(max_length=100, verbose_name='Nome do Vídeo')
    ano_publicacao = models.IntegerField()
    colecao = models.CharField(max_length=100, verbose_name='Coleção')
    qtvideos = models.BigIntegerField(verbose_name='Quantidade de Vídeos')
    estante = models.CharField(max_length=50, blank=True, verbose_name='Nome da Estante')
    observacao = models.CharField(max_length=100, blank=True, verbose_name='Observação')
    data_cadastro = models.DateField(default=timezone.now, verbose_name='Data do Cadastro')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return self.nome_video

    class Meta:
        ordering = ['nome_video']
        verbose_name = "Cadastro de Vídeos"
        verbose_name_plural = "Cadastro de Vídeos"

class Clientes(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100, verbose_name='Nome do Usuário')
    email = models.EmailField(unique=True, verbose_name='E-mail', blank=True)
    documento = models.CharField(max_length=30, unique=True, verbose_name='Número do Documento', blank=True)
    situacao = models.CharField(max_length=30, verbose_name='Situação ', blank=True)
    serie = models.CharField(max_length=30, verbose_name='Série ', blank=True)
    nr_telefone = models.CharField(max_length=30, unique=True, blank=True, verbose_name='Número do Telefone')
    tipo_usuario = models.CharField(max_length=30, choices=[
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('pesquisador', 'Pesquisador'),
        ('outros', 'Outros'),
    ], default='aluno', verbose_name='Tipo de Usuário')
    cpf = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^\d{11}$', message='CPF deve ter 11 dígitos')],
        unique=True, blank=True
    )

    def save(self, *args, **kwargs):
        cpf_validator = CPF()
        if not cpf_validator.validate(self.cpf):
            raise ValidationError('CPF inválido.')
        super().save(*args, **kwargs)

    cep = models.CharField(
        max_length=8,
        verbose_name='CEP do Imóvel',
        blank=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='CEP deve ter 8 dígitos')]
    )
    logradouro = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    nr_imovel = models.CharField(max_length=10, verbose_name='Número do Imóvel', blank=True)
    observacao = models.TextField(max_length=100, blank=True, verbose_name='Observação: ')
    erro_cep = models.CharField(max_length=255, blank=True, verbose_name='Erro ao buscar o CEP')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def preencher_endereco_por_cep(self, request=None):
        try:

            self.cep = self.cep.strip().replace('-', '')
            print(f"CEP formatado: {self.cep}")
            url = f'https://viacep.com.br/ws/{self.cep}/json/'
            response = requests.get(url, timeout=10)

            print(f"Status da resposta: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Dados recebidos da API: {data}")

                # Force a return to see if the problem is in the data processing
                self.logradouro = data.get('logradouro', 'Logradouro forçado')
                self.bairro = data.get('bairro', 'Bairro forçado')
                self.cidade = data.get('localidade', 'Cidade forçada')
                self.estado = data.get('uf', 'UF forçada')

                print(f"Logradouro: {self.logradouro}")
                print(f"Bairro: {self.bairro}")
                print(f"Cidade: {self.cidade}")
                print(f"Estado: {self.estado}")

                if not all([self.logradouro, self.bairro, self.cidade, self.estado]):
                    self.erro_cep = 'CEP não encontrado ou dados incompletos.'
                    print(f"Erro: {self.erro_cep}")
                    if request:
                        print(f"Adicionando mensagem de erro: {self.erro_cep}")
                        messages.error(request, self.erro_cep)
                else:
                    self.erro_cep = ''
                    print("Endereço preenchido corretamente.")
            else:
                self.erro_cep = f"Erro na consulta do CEP: {response.status_code}"
                print(f"Erro na resposta da API: {self.erro_cep}")
                if request:
                    print(f"Adicionando mensagem de erro: {self.erro_cep}")
                    messages.error(request, self.erro_cep)

        except requests.exceptions.RequestException as e:
            self.erro_cep = f"Erro na requisição: {e}"
            print(f"Erro na requisição: {self.erro_cep}")
            if request:
                print(f"Adicionando mensagem de erro: {self.erro_cep}")
                messages.error(request, self.erro_cep)

        if self.erro_cep:
            self.logradouro = ''
            self.bairro = ''
            self.cidade = ''
            self.estado = ''

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        self.preencher_endereco_por_cep(request)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_cliente if self.nome_cliente else 'Nome do Requisitante'

    class Meta:
        ordering = ['nome_cliente']
        verbose_name = "Nome do Requisitante"
        verbose_name_plural = "Requisitantes"

class Reservas(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    titulo = models.ForeignKey(Livros, on_delete=models.CASCADE, verbose_name='Livro')
    nome_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Cliente')
    data_reserva = models.DateField(default=timezone.now, verbose_name='Data da Reserva')
    data_retirada = models.DateField(null=True, blank=True, verbose_name='Data de Retirada')
    data_devolucao = models.DateField(null=True, blank=True, verbose_name='Data de Devolução')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def __str__(self):
        return f'{self.titulo} - {self.nome_cliente}'

    class Meta:
        ordering = ['data_reserva']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

class EmprestimoLivro(models.Model):
    emprestimo_id = models.AutoField(primary_key=True)
    titulo = models.ForeignKey(Livros, on_delete=models.CASCADE, verbose_name='Livro')
    nome_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Cliente')
    data_emprestimo = models.DateField(default=timezone.now, verbose_name='Data do Empréstimo')
    data_devolucao = models.DateField(null=True, blank=True, verbose_name='Data da Devolução')
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name='Multa')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')  # Chave estrangeira para a tabela Escola

    def save(self, *args, **kwargs):
        # Verificação de data de devolução no futuro
        if self.data_devolucao:
            hoje = timezone.now().date()
            if self.data_devolucao > hoje:
                raise ValidationError('Data de devolução não pode ser no futuro.')
            prazo = (self.data_devolucao - self.data_emprestimo).days
            if prazo > 30:  # Exemplo de prazo
                dias_atraso = (hoje - self.data_devolucao).days
                self.multa = dias_atraso * 1.00  # Exemplo de multa diária

        # Verificação de estoque antes de realizar o empréstimo
        if not self.pk:  # Se é um novo empréstimo
            # Garantir que qtlivros é um número
            if self.titulo.qtlivros is None:
                self.titulo.qtlivros = 0  # Define qtlivros como 0 se for None
            elif isinstance(self.titulo.qtlivros, str):
                self.titulo.qtlivros = int(self.titulo.qtlivros)  # Converte string para inteiro

            if self.titulo.qtlivros <= 0:
                raise ValidationError('Não há exemplares deste livro em estoque.')
            self.titulo.qtlivros -= 1
            self.titulo.save()

        super().save(*args, **kwargs)

        # Incrementa o estoque após a devolução
        if self.data_devolucao:
            if self.titulo.qtlivros is None:
                self.titulo.qtlivros = 0  # Define qtlivros como 0 se for None
            elif isinstance(self.titulo.qtlivros, str):
                self.titulo.qtlivros = int(self.titulo.qtlivros)  # Converte string para inteiro

            self.titulo.qtlivros += 1
            self.titulo.save()

    def __str__(self):
        return f'{self.titulo} - {self.nome_cliente}'

    class Meta:
        ordering = ['data_emprestimo']
        verbose_name = "Empréstimo de Livros"
        verbose_name_plural = "Empréstimos de Livros"

class EmprestimoVideo(models.Model):
    emprestimo_id = models.AutoField(primary_key=True)
    nome_video = models.ForeignKey(Videos, on_delete=models.CASCADE, verbose_name='Vídeo')
    nome_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Cliente')
    data_emprestimo = models.DateField(default=timezone.now, verbose_name='Data do Empréstimo')
    data_devolucao = models.DateField(null=True, blank=True, verbose_name='Data da Devolução')
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name='Multa')
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, verbose_name='Escola')

    def save(self, *args, **kwargs):
        hoje = timezone.now().date()

        # Verificação de estoque ao criar um novo empréstimo
        if not self.pk:  # Se é um novo empréstimo
            if self.nome_video.qtvideos <= 0:
                raise ValidationError('Não há vídeos em estoque para este título.')
            self.nome_video.qtvideos -= 1  # Reduz o estoque
            self.nome_video.save()  # Atualiza o vídeo

        super().save(*args, **kwargs)

        # Se a devolução for registrada
        if self.data_devolucao and not hasattr(self, '_estoque_atualizado'):
            # Incrementa o estoque após a devolução
            self.nome_video.qtvideos += 1
            self.nome_video.save()

            # Evita que o estoque seja incrementado mais de uma vez
            self._estoque_atualizado = True

    def __str__(self):
        return f'{self.nome_video} - {self.nome_cliente}'

    class Meta:
        ordering = ['data_emprestimo']
        verbose_name = "Empréstimo de Vídeo"
        verbose_name_plural = "Empréstimos de Vídeos"
