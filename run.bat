@echo off
echo Iniciando Gestion de Ventas...
echo.

REM Cambiar al directorio donde está este BAT
cd /d "%~dp0"

REM Activar el entorno virtual
call .venv\Scripts\activate.bat

REM Ejecutar el programa correctamente como módulo
python -m src.main

echo.
echo Programa finalizado.
pause
