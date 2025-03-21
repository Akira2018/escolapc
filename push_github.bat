
@echo off
REM Script para fazer push para o GitHub

echo.
echo ===== Fazendo commit das alterações =====
git add .
git commit -m "Atualizações finais e sincronização com GitHub"

echo.
echo ===== Fazendo push para o GitHub =====
git push origin main

echo.
echo ===== Push para o GitHub concluído com sucesso! =====
pause
