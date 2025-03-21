
@echo off
REM Script para rodar migrações e abrir app no Heroku

echo.
echo ===== Aplicando migrações no Heroku =====
heroku run python manage.py migrate --app escolapc

echo.
echo ===== Abrindo aplicativo no navegador =====
start https://escolapc-eef942cb2e5c.herokuapp.com/

echo.
echo ===== Deseja reativar collectstatic? =====
echo (Aperte S para Sim ou qualquer tecla para sair)
set /p opcao="Deseja reativar collectstatic (S/N)? "

IF /I "%opcao%"=="S" (
    heroku config:unset DISABLE_COLLECTSTATIC --app escolapc
    echo.
    echo ===== collectstatic reativado com sucesso! =====
)

echo.
echo ===== Processo concluído! =====
pause
