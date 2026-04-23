#!/bin/bash
# Script para criar ambiente virtual e instalar dependências (Linux/Mac)

if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
else
    echo "Ambiente virtual já existe."
fi

# Ativa o ambiente virtual
source .venv/bin/activate

# Instala dependências
pip install -r requirements.txt

echo "Ambiente pronto!"
