#!/bin/bash

# Script de instalación para phonk-trigger

echo "Bienvenido al instalador de phonk-trigger"
echo "Este script instalará las dependencias necesarias y configurará el programa."
echo ""

# Verificar si estamos en Ubuntu
if ! grep -q "Ubuntu" /etc/os-release; then
    echo "Este script está diseñado para Ubuntu. Saliendo..."
    exit 1
fi

# Obtener MP3_DIR del argumento o pedirlo
if [ -n "$1" ]; then
    MP3_DIR="$1"
else
    echo "Por favor, introduce la ruta completa al directorio que contiene los archivos MP3:"
    read -r MP3_DIR
fi

# Validar que la ruta existe
if [ ! -d "$MP3_DIR" ]; then
    echo "La ruta especificada no existe o no es un directorio. Saliendo..."
    exit 1
fi

# Instalar dependencias del sistema
echo "Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv qttools5-dev-tools

# Instalar Poetry si no está instalado
if ! command -v poetry &> /dev/null; then
    echo "Instalando Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    source $HOME/.bashrc
fi

# Instalar dependencias de Python con Poetry
echo "Instalando dependencias de Python..."
$HOME/.local/bin/poetry install

# Crear o actualizar config_phonk.json
echo "Configurando config_phonk.json..."
cat > config_phonk.json << EOF
{
    "mp3_dir": "$MP3_DIR"
}
EOF

echo ""
echo "Instalación completada exitosamente!"
echo ""
echo "Para ejecutar el programa, copia y pega los siguientes comandos:"
echo ""
echo "cd $(pwd)"
echo "$HOME/.local/bin/poetry run python phonk_script.py"
echo ""
echo "Nota: Asegúrate de que el directorio MP3 contiene archivos .mp3 válidos."
