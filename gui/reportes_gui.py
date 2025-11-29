"""
GUI para Reportes y Gráficas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from gui.graficas import VentanaGraficas


class ReportesFrame(ttk.Frame):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.bd = bd
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de reportes"""
        
        # Título
        titulo = ttk.Label(self, text="Reportes y Análisis", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame de botones reportes
        frame_botones1 = ttk.Frame(self)
        frame_botones1.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame_botones1, text="Ventas del Día", command=self.reporte_ventas_dia).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones1, text="Stock Bajo", command=self.reporte_stock_bajo).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones1, text="Más Vendidos", command=self.reporte_mas_vendidos).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones1, text="Menos Vendidos", command=self.reporte_menos_vendidos).pack(side=tk.LEFT, padx=2)
        
        # Frame de botones gráficas
        frame_botones2 = ttk.Frame(self)
        frame_botones2.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_botones2, text="Gráficas:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.graficas = VentanaGraficas(self.bd)
        
        ttk.Button(frame_botones2, text="📊 Ventas por Hora", command=self.graficas.grafica_ventas_por_hora).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones2, text="📈 Producto Top", command=self.graficas.grafica_producto_mas_vendido).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones2, text="🏆 Categorías", command=self.graficas.grafica_categorias_mas_vendidas).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones2, text="📉 Tendencia Mes", command=self.graficas.grafica_tendencia_ventas_mes).pack(side=tk.LEFT, padx=2)
        
        # Frame para tabla
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_reporte = ttk.Treeview(frame_tabla, yscrollcommand=scrollbar.set)
        self.tree_reporte.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree_reporte.yview)
    
    def reporte_ventas_dia(self):
        """Muestra las ventas del día actual"""
        fecha = datetime.now().date()
        
        sql = """
            SELECT 
                v.id,
                v.fecha,
                v.hora,
                v.total,
                v.metodo_pago,
                COUNT(dv.id) as cantidad_productos
            FROM ventas v
            LEFT JOIN detalle_ventas dv ON v.id = dv.venta_id
            WHERE DATE(v.fecha) = %s
            GROUP BY v.id
            ORDER BY v.hora
        """
        
        ventas = self.bd.ejecutar_consulta(sql, (fecha,))
        
        # Limpiar tabla
        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        
        if ventas:
            # Configurar columnas
            self.tree_reporte['columns'] = ('Factura', 'Hora', 'Total', 'Método', 'Productos')
            self.tree_reporte['show'] = 'headings'
            
            self.tree_reporte.column('Factura', width=80)
            self.tree_reporte.column('Hora', width=100)
            self.tree_reporte.column('Total', width=100)
            self.tree_reporte.column('Método', width=100)
            self.tree_reporte.column('Productos', width=100)
            
            self.tree_reporte.heading('Factura', text='Factura')
            self.tree_reporte.heading('Hora', text='Hora')
            self.tree_reporte.heading('Total', text='Total')
            self.tree_reporte.heading('Método', text='Método')
            self.tree_reporte.heading('Productos', text='Productos')
            
            total_ventas = 0
            for venta in ventas:
                self.tree_reporte.insert('', tk.END, values=(
                    venta['id'],
                    str(venta['hora']),
                    f"${venta['total']:.2f}",
                    venta['metodo_pago'],
                    venta['cantidad_productos']
                ))
                total_ventas += venta['total']
            
            self.tree_reporte.insert('', tk.END, values=('', 'TOTAL', f"${total_ventas:.2f}", '', len(ventas)))
        else:
            messagebox.showinfo("Información", "No hay ventas para hoy")
    
    def reporte_stock_bajo(self):
        """Muestra productos con stock bajo"""
        sql = """
            SELECT 
                p.id,
                p.nombre,
                c.nombre as categoria,
                p.stock,
                p.stock_minimo
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock <= p.stock_minimo AND p.activo = TRUE
            ORDER BY p.stock ASC
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        # Limpiar tabla
        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        
        if productos:
            self.tree_reporte['columns'] = ('ID', 'Producto', 'Categoría', 'Stock', 'Mínimo')
            self.tree_reporte['show'] = 'headings'
            
            self.tree_reporte.column('ID', width=50)
            self.tree_reporte.column('Producto', width=200)
            self.tree_reporte.column('Categoría', width=100)
            self.tree_reporte.column('Stock', width=80)
            self.tree_reporte.column('Mínimo', width=80)
            
            self.tree_reporte.heading('ID', text='ID')
            self.tree_reporte.heading('Producto', text='Producto')
            self.tree_reporte.heading('Categoría', text='Categoría')
            self.tree_reporte.heading('Stock', text='Stock')
            self.tree_reporte.heading('Mínimo', text='Mínimo')
            
            for prod in productos:
                self.tree_reporte.insert('', tk.END, values=(
                    prod['id'],
                    prod['nombre'],
                    prod['categoria'],
                    prod['stock'],
                    prod['stock_minimo']
                ), tags=('stock_bajo',))
            
            self.tree_reporte.tag_configure('stock_bajo', background='#ffcccc')
        else:
            messagebox.showinfo("Información", "No hay productos con stock bajo")
    
    def reporte_mas_vendidos(self):
        """Muestra los productos más vendidos"""
        sql = """
            SELECT 
                p.id,
                p.nombre,
                SUM(dv.cantidad) as total_vendido,
                SUM(dv.subtotal) as ingresos
            FROM productos p
            JOIN detalle_ventas dv ON p.id = dv.producto_id
            WHERE p.activo = TRUE
            GROUP BY p.id
            ORDER BY total_vendido DESC
            LIMIT 20
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        # Limpiar tabla
        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        
        if productos:
            self.tree_reporte['columns'] = ('ID', 'Producto', 'Vendido', 'Ingresos')
            self.tree_reporte['show'] = 'headings'
            
            self.tree_reporte.column('ID', width=50)
            self.tree_reporte.column('Producto', width=250)
            self.tree_reporte.column('Vendido', width=100)
            self.tree_reporte.column('Ingresos', width=150)
            
            self.tree_reporte.heading('ID', text='ID')
            self.tree_reporte.heading('Producto', text='Producto')
            self.tree_reporte.heading('Vendido', text='Unidades')
            self.tree_reporte.heading('Ingresos', text='Ingresos')
            
            for prod in productos:
                self.tree_reporte.insert('', tk.END, values=(
                    prod['id'],
                    prod['nombre'],
                    prod['total_vendido'],
                    f"${prod['ingresos']:.2f}"
                ))
        else:
            messagebox.showinfo("Información", "No hay datos de ventas")
    
    def reporte_menos_vendidos(self):
        """Muestra los productos menos vendidos"""
        sql = """
            SELECT 
                p.id,
                p.nombre,
                COALESCE(SUM(dv.cantidad), 0) as total_vendido
            FROM productos p
            LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
            WHERE p.activo = TRUE
            GROUP BY p.id
            ORDER BY total_vendido ASC
            LIMIT 20
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        # Limpiar tabla
        for item in self.tree_reporte.get_children():
            self.tree_reporte.delete(item)
        
        if productos:
            self.tree_reporte['columns'] = ('ID', 'Producto', 'Vendido')
            self.tree_reporte['show'] = 'headings'
            
            self.tree_reporte.column('ID', width=50)
            self.tree_reporte.column('Producto', width=300)
            self.tree_reporte.column('Vendido', width=100)
            
            self.tree_reporte.heading('ID', text='ID')
            self.tree_reporte.heading('Producto', text='Producto')
            self.tree_reporte.heading('Vendido', text='Unidades')
            
            for prod in productos:
                self.tree_reporte.insert('', tk.END, values=(
                    prod['id'],
                    prod['nombre'],
                    prod['total_vendido']
                ))
        else:
            messagebox.showinfo("Información", "No hay datos de productos")
