@echo off
REM Script para criar ambiente virtual e instalar dependências

if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
) else (
    echo Ambiente virtual já existe.
)

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Instala dependências
pip install -r requirements.txt

echo Ambiente pronto!
