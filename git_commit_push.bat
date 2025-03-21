
@echo off
REM Script para automatizar git add, commit e push

echo.
set /p commitMsg="Digite a mensagem do commit: "

echo.
echo ===== Adicionando arquivos =====
git add .

echo.
echo ===== Fazendo commit =====
git commit -m "%commitMsg%"

echo.
echo ===== Enviando para o GitHub =====
git push origin main

echo.
echo ===== Processo concluído com sucesso! =====
pause
