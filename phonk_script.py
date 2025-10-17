#!/usr/bin/env python3
import sys
import os
import random
import subprocess
import time
import threading
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from pynput import mouse, keyboard
import pygame

# Load configuration
with open('config_phonk.json', 'r') as f:
    config = json.load(f)
MP3_DIR = config.get('mp3_dir', '')
EFFECT_MS = 3000  # 3 segundos


# ---------- Funciones de efecto ----------
def toggle_kwin_desaturate():
    """Activa o desactiva el filtro blanco y negro de KDE (KWin)."""
    subprocess.run(
        [
            "qdbus",
            "org.kde.KWin",
            "/Compositor",
            "toggleEffect",
            "kwin4_effect_desaturate",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def start_bw_filter():
    toggle_kwin_desaturate()


def stop_bw_filter():
    toggle_kwin_desaturate()


# ---------- Ventanita con calavera ----------
class SkullPopup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Tool
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0);"
        )  # Asegurar transparencia
        label = QtWidgets.QLabel("💀", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 0);"
        )  # Texto blanco, bg transparente
        font = QtGui.QFont()
        font.setPointSize(120)
        label.setFont(font)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        self.resize(300, 300)
        self.center_on_screen()

    def center_on_screen(self):
        scr = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(
            scr.center().x() - self.width() // 2, scr.center().y() - self.height() // 2
        )


# ---------- Gestor de efectos ----------
class EffectManager(QtCore.QObject):
    effect_triggered = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.active_effect = False
        self.popup = None
        self.effect_triggered.connect(self.start_effect)

    def trigger_effect(self):
        if not self.active_effect and random.random() <= 0.10:
            self.effect_triggered.emit()

    def start_effect(self):
        self.active_effect = True
        # Filtro blanco y negro (KWin)
        start_bw_filter()

        # Ventanita 💀
        self.popup = SkullPopup()
        self.popup.show()

        # Reproducir audio
        if os.path.exists(MP3_DIR):
            mp3_files = [f for f in os.listdir(MP3_DIR) if f.endswith(".mp3")]
            if mp3_files:
                random_mp3 = random.choice(mp3_files)
                mp3_path = os.path.join(MP3_DIR, random_mp3)
                try:
                    pygame.mixer.music.load(mp3_path)
                    pygame.mixer.music.play()
                except Exception as e:
                    print("Error de audio:", e)

        # Parar después de 3 s
        QtCore.QTimer.singleShot(EFFECT_MS, self.stop_effect)

    def stop_effect(self):
        # Detener audio
        pygame.mixer.music.stop()
        # Quitar filtro
        stop_bw_filter()
        # Cerrar ventana
        if self.popup:
            self.popup.close()
            self.popup = None
        self.active_effect = False


# ---------- Listeners globales ----------
def on_mouse_click(x, y, button, pressed):
    if pressed:
        global manager
        manager.trigger_effect()


def on_key_press(key):
    global manager
    manager.trigger_effect()


# ---------- Main ----------
def main():
    # Audio init
    pygame.mixer.init()

    # QApplication para Qt
    app = QtWidgets.QApplication(sys.argv)

    # Crear gestor de efectos
    global manager
    manager = EffectManager()

    # Iniciar listeners en hilo separado
    mouse_listener = mouse.Listener(on_click=on_mouse_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)

    mouse_listener.start()
    keyboard_listener.start()

    # Ejecutar event loop de Qt
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
