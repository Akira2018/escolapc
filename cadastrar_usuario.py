import os
import django
<<<<<<< HEAD
<<<<<<< HEAD
import getpass

# Configura o Django para acessar o banco de dados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_proj.settings')  # Substitua pelo nome correto do seu projeto
=======

# Configura o Django para acessar o banco de dados e os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_proj.settings')  # Substitua 'gestao_proj' pelo nome correto do seu projeto
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======

# Configura o Django para acessar o banco de dados e os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_proj.settings')  # Substitua 'gestao_proj' pelo nome correto do seu projeto
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
django.setup()

from gestao.models import User  # Importa o modelo de usuário personalizado
from django.contrib.auth.models import Group

def cadastrar_usuario():
<<<<<<< HEAD
<<<<<<< HEAD
    username = input("Digite o nome de usuário: ").strip()
    if not username:
        print("O nome de usuário não pode estar vazio.")
        return

    if User.objects.filter(username=username).exists():
        print(f"Erro: O nome de usuário '{username}' já existe. Escolha outro.")
        return

    password = getpass.getpass("Digite a senha: ")
    confirm_password = getpass.getpass("Confirme a senha: ")

    if password != confirm_password:
        print("Erro: As senhas não coincidem.")
        return

    confirmacao = input(f"Tem certeza que deseja criar o usuário '{username}'? (S/N): ").strip().lower()
    if confirmacao != 's':
        print("Operação cancelada.")
        return

    novo_usuario = User.objects.create_user(username=username, password=password)
    print(f"Usuário '{username}' criado com sucesso.")

    grupos = Group.objects.all()
    if not grupos.exists():
        print("Nenhum grupo encontrado. O usuário foi criado sem grupo.")
        return

    print("\nGrupos disponíveis:")
    for i, grupo in enumerate(grupos, start=1):
        print(f"{i}. {grupo.name}")

    while True:
        try:
            grupo_escolhido = int(input("\nDigite o número do grupo para adicionar o usuário (ou 0 para pular): "))
            if grupo_escolhido == 0:
                print("Usuário criado sem grupo.")
                return

            grupo = grupos[grupo_escolhido - 1]
            break
        except (IndexError, ValueError):
            print("Opção inválida. Tente novamente.")

    novo_usuario.groups.add(grupo)
    novo_usuario.save()
    print(f"Usuário '{username}' foi adicionado ao grupo '{grupo.name}'.")

if __name__ == "__main__":
    cadastrar_usuario()
=======
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
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
<<<<<<< HEAD
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
=======
>>>>>>> 145c46dcb5b19a9082f2e39ee66b3b5564513083
