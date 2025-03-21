
@echo off
echo.
echo ===== Instalando django-cors-headers =====
pip install django-cors-headers

echo.
echo ===== Atualizando requirements.txt =====
pip freeze > requirements.txt

echo.
echo ===== Fazendo commit =====
git add requirements.txt
git commit -m "Adicionando django-cors-headers"

echo.
echo ===== Enviando para o GitHub =====
git push origin main

echo.
echo ===== Enviando para o Heroku =====
git push heroku main --force

echo.
echo ===== Rodando migrações no Heroku =====
heroku run python manage.py migrate --app escolapc

echo.
echo ===== Processo concluído! =====
pause
