import pandas as pd
from gestao.models import Livros, Autores, Editoras, Generos, Assuntos

class Command(BaseCommand):
    help = 'Importa dados do Excel para o banco de dados'

    def handle(self, *args, **kwargs):
        df = pd.read_csv(r'D:\BibliotecaPI02\Importacao_Livros.csv', delimiter=';')

        for index, row in df.iterrows():
            autor, created = Autores.objects.get_or_create(nome_autor=row['nome_autor'])
            editora, created = Editoras.objects.get_or_create(nome_editora=row['nome_editora'])

            livro = Livros(
                titulo=row['Titulo'],
                nome_autor=autor,
                nome_editora=editora,
                isbn=row.get('isbn'),
                edicao=row.get('edicao'),
                ano_publicacao=row.get('ano_publicacao'),
                qtlivros=row.get('qtlivros'),
                localizacao=row.get('localizacao'),
                descricao=row.get('descricao'),
            )
            livro.save()

            if 'nome_genero' in row and row['nome_genero']:
                generos = row['nome_genero'].split(',')
                for genero_nome in generos:
                    genero, created = Generos.objects.get_or_create(nome=genero_nome.strip())
                    livro.nome_genero.add(genero)

            if 'descr_assunto' in row and row['descr_assunto']:
                assuntos = row['descr_assunto'].split(',')
                for assunto_nome in assuntos:
                    assunto, created = Assuntos.objects.get_or_create(nome=assunto_nome.strip())
                    livro.descr_assunto.add(assunto)

            livro.save()

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
