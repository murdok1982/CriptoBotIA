#!/bin/bash

echo "🚀 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Dependencias instaladas. Lanzando el bot..."
python run_bot.py
