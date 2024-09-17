import os
import django

# Configura o Django para acessar o banco de dados e os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_proj.settings')  # Substitua 'gestao_proj' pelo nome correto do seu projeto
django.setup()

from gestao.models import User  # Importa o modelo de usuário personalizado
from django.contrib.auth.models import Group

def cadastrar_usuario():
    # Solicita o nome de usuário e a senha para cadastro
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")

    # Verifica se o nome de usuário já existe
    if User.objects.filter(username=username).exists():
        print(f"O nome de usuário '{username}' já existe. Escolha outro.")
        return

    # Crie um novo usuário com o nome de usuário e senha fornecidos
    novo_usuario = User.objects.create_user(username=username, password=password)
    print(f"Usuário '{username}' criado com sucesso.")

    # Exibe a lista de grupos disponíveis
    grupos = Group.objects.all()
    print("Grupos disponíveis:")
    for i, grupo in enumerate(grupos):
        print(f"{i + 1}. {grupo.name}")

    # Solicita que o usuário escolha um grupo
    grupo_escolhido = int(input("Digite o número do grupo que deseja adicionar o usuário: ")) - 1

    try:
        grupo = grupos[grupo_escolhido]
    except IndexError:
        print("Opção de grupo inválida.")
        return

    # Adiciona o novo usuário ao grupo escolhido
    novo_usuario.groups.add(grupo)

    # Salve as mudanças no usuário
    novo_usuario.save()

    print(f"O usuário '{username}' foi adicionado ao grupo '{grupo.name}'.")

# Chama a função para cadastro de usuário
cadastrar_usuario()
