"""
Punto de Entrada Principal
Mini Super Las Botargas - Sistema de Punto de Venta
"""

import sys
import os

# Agregar ruta al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.app import VentanaPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()
