@echo off
REM Inicia a aplicação Zapp Valores em Divida
REM Porta: 8004
REM Host: 0.0.0.0 (acessível na rede)

echo.
echo ========================================
echo Zapp Valores em Divida
echo ========================================
echo Porta: 8004
echo Host: 0.0.0.0 (Rede)
echo.
echo Para aceder localmente: http://localhost:8004
echo Para aceder pela rede: http://%COMPUTERNAME%:8004
echo ou substitua %COMPUTERNAME% pelo IP da máquina
echo.
echo Pressione qualquer tecla para iniciar...
pause > nul

cd /d "%~dp0"

REM Verificar se existe venv
if not exist "venv\Scripts\activate.bat" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv e instalar dependências
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Iniciar a aplicação
echo Iniciando a aplicação...
python backend\main.py
