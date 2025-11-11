#!/bin/bash

# Criar e ativar virtual environment
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrations
python manage.py migrate

# Criar superuser (opcional)
# python manage.py createsuperuser

echo "Setup completo! Execute: python manage.py runserver"
