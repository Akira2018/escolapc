
@echo off
REM Script para recriar ambiente virtual, reinstalar dependências e corrigir push no Heroku

echo.
echo ===== Apagando ambiente virtual antigo =====
rmdir /s /q venv

echo.
echo ===== Criando novo ambiente virtual =====
python -m venv venv

echo.
echo ===== Ativando ambiente virtual =====
call venv\Scripts\activate

echo.
echo ===== Instalando dependências principais =====
pip install django django-heroku django-cors-headers django-grappelli

echo.
echo ===== Atualizando requirements.txt =====
pip freeze > requirements.txt

echo.
echo ===== Fazendo commit das dependências corrigidas =====
git add requirements.txt
git commit -m "Corrigindo ambiente virtual e dependências"

echo.
echo ===== Fazendo push para o Heroku =====
git push heroku main

echo.
echo ===== Processo concluído com sucesso! =====
pause
