
@echo off
REM Script para automatizar git add, commit e push com caminho completo do Git

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
echo ===== Processo concluído com sucesso! =====
pause
