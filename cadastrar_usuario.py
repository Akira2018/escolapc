import os
import django
import getpass

# Configura o Django para acessar o banco de dados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_proj.settings')  # Substitua pelo nome correto do seu projeto
django.setup()

from gestao.models import User  # Importa o modelo de usuário personalizado
from django.contrib.auth.models import Group

def cadastrar_usuario():
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
