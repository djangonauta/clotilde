@echo off
echo Iniciando Clotilde em modo debug...
clotilde.exe > debug_output.log 2>&1
echo Aplicação encerrada. Verifique o arquivo debug_output.log
pause