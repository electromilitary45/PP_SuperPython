"""
Ventana principal de la aplicación Tkinter
Mini Super Las Botargas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gui.productos_gui import ProductosFrame
from gui.ventas_gui import VentasFrame
from gui.reportes_gui import ReportesFrame
from database.conexion import ConexionBD
from config import HOST, USUARIO, CONTRASEÑA, BASE_DATOS


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Super Las Botargas - Sistema de Punto de Venta")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f0f0f0")
        # Maximizar ventana al inicio
        self.root.state('zoomed')
        
        # Conexión a BD
        self.bd = ConexionBD(HOST, USUARIO, CONTRASEÑA, BASE_DATOS)
        
        # Intentar conexión
        if not self.bd.conectar():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        
        # Encabezado
        encabezado = tk.Frame(self.root, bg="#2c3e50", height=80)
        encabezado.pack(fill=tk.X)
        
        tk.Label(
            encabezado,
            text="MINI SUPER LAS BOTARGAS",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=10)
        
        tk.Label(
            encabezado,
            text="Sistema de Punto de Venta",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack()
        
        # Contenedor principal con notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas
        frame_productos = ProductosFrame(notebook, self.bd)
        frame_ventas = VentasFrame(notebook, self.bd)
        frame_reportes = ReportesFrame(notebook, self.bd)
        
        notebook.add(frame_productos, text="Productos")
        notebook.add(frame_ventas, text="Punto de Venta")
        notebook.add(frame_reportes, text="Reportes")
        
        # Pie de página
        pie = tk.Frame(self.root, bg="#2c3e50", height=50)
        pie.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            pie,
            text="© 2025 Mini Super Las Botargas | Sistema de Gestión de Ventas",
            bg="#2c3e50",
            fg="#95a5a6",
            font=("Arial", 9)
        ).pack(pady=5)
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación correctamente"""
        self.bd.desconectar()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()
