script.bat


@echo off

:: Script para instalar todas as dependências do projeto escolapc
echo ===============================================
echo   INICIANDO INSTALAÇÃO DAS BIBLIOTECAS...
echo ===============================================

:: Cria e ativa o ambiente virtual (opcional)
python -m venv venv
call venv\Scripts\activate

:: Instala bibliotecas principais
pip install -r requirements.txt

:: Instala adicionais
pip install django-debug-toolbar
pip install whitenoise
pip install gunicorn
pip install requests
pip install python-docx
pip install django-cors-headers
pip install django-grappelli
pip install django-heroku
pip install python-dotenv
pip install validate-docbr

:: Atualiza requirements.txt
pip freeze > requirements.txt

:: Coleta arquivos estáticos
python manage.py collectstatic --noinput

echo ===============================================
echo   INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ===============================================

pause
