
@echo off
REM Script para commit + push para GitHub e Heroku

echo.
set /p commitMsg="Digite a mensagem do commit: "

echo.
echo ===== Adicionando arquivos =====
"C:\Program Files\Git\bin\git.exe" add .

echo.
echo ===== Fazendo commit =====
"C:\Program Files\Git\bin\git.exe" commit -m "%commitMsg%"

echo.
echo ===== Enviando para o GitHub =====
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ===== Enviando para o Heroku =====
"C:\Program Files\Git\bin\git.exe" push heroku main

echo.
echo ===== Processo concluído com sucesso! =====
pause
