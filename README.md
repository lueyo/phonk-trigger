# phonk-trigger
Un script que se ejecuta en segundo plano y cuando pulses una tecla o des click hay un 10% de posibilidades de que salga una calavera y se ejecute musica phonk por 3 segundos

## Compatibilidad
Este programa está diseñado y probado únicamente en **Ubuntu con KDE y X11**. No se garantiza el funcionamiento en otros sistemas operativos, entornos de escritorio o gestores de ventanas.

## Instalación
Copia y pega los siguientes comandos para clonar el repositorio e instalar el programa:

```bash
git clone https://github.com/lueyo/phonk-trigger.git
cd phonk-trigger
./install.sh
```

El script de instalación configurará automáticamente todas las dependencias y te pedirá la ruta al directorio que contiene los archivos MP3. Alternativamente, puedes pasar la ruta como argumento para evitar la interacción:

```bash
./install.sh /ruta/a/tu/directorio/mp3
```

## Ejecución
Después de la instalación, copia y pega los comandos proporcionados por el script de instalación para ejecutar el programa.

Ejemplo:
```bash
cd /ruta/al/proyecto
poetry run python phonk_script.py
```
