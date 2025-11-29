"""
Módulo de gráficas y visualizaciones
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


class VentanaGraficas:
    """Ventana para mostrar gráficas avanzadas"""
    
    def __init__(self, bd):
        self.bd = bd
        self.ventana = None
    
    def grafica_ventas_por_hora(self):
        """Muestra las ventas por hora del día"""
        ventana = tk.Toplevel()
        ventana.title("Ventas por Hora del Día")
        ventana.geometry("800x500")
        
        # Obtener datos
        fecha = datetime.now().date()
        sql = """
            SELECT 
                HOUR(v.hora) as hora,
                COUNT(*) as cantidad,
                SUM(v.total) as total
            FROM ventas v
            WHERE DATE(v.fecha) = %s
            GROUP BY HOUR(v.hora)
            ORDER BY hora
        """
        
        datos = self.bd.ejecutar_consulta(sql, (fecha,))
        
        if not datos:
            messagebox.showinfo("Información", "No hay datos de ventas para hoy")
            return
        
        # Preparar datos para gráfica
        horas = [f"{d['hora']:02d}:00" for d in datos]
        ventas = [d['total'] for d in datos]
        
        # Crear figura
        fig = Figure(figsize=(10, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        ax.bar(horas, ventas, color='#3498db', edgecolor='#2c3e50', linewidth=2)
        ax.set_xlabel('Hora del Día', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total de Ventas ($)', fontsize=12, fontweight='bold')
        ax.set_title('Ventas por Hora - Día de Hoy', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Agregar valores sobre las barras
        for i, v in enumerate(ventas):
            ax.text(i, v + 5, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Rotar eje x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Embedder en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafica_producto_mas_vendido(self):
        """Muestra tendencia del producto más vendido"""
        # Obtener el producto más vendido este mes
        sql = """
            SELECT 
                p.id,
                p.nombre,
                SUM(dv.cantidad) as total
            FROM productos p
            JOIN detalle_ventas dv ON p.id = dv.producto_id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE MONTH(v.fecha) = MONTH(NOW()) AND YEAR(v.fecha) = YEAR(NOW())
            GROUP BY p.id
            ORDER BY total DESC
            LIMIT 1
        """
        
        producto_top = self.bd.ejecutar_consulta(sql)
        
        if not producto_top:
            messagebox.showinfo("Información", "No hay ventas este mes")
            return
        
        producto_id = producto_top[0]['id']
        producto_nombre = producto_top[0]['nombre']
        
        # Obtener datos diarios
        sql_dias = """
            SELECT 
                DATE(v.fecha) as fecha,
                SUM(dv.cantidad) as cantidad,
                SUM(dv.subtotal) as ingresos
            FROM detalle_ventas dv
            JOIN ventas v ON dv.venta_id = v.id
            WHERE dv.producto_id = %s
            AND MONTH(v.fecha) = MONTH(NOW())
            AND YEAR(v.fecha) = YEAR(NOW())
            GROUP BY DATE(v.fecha)
            ORDER BY fecha
        """
        
        datos = self.bd.ejecutar_consulta(sql_dias, (producto_id,))
        
        if not datos:
            messagebox.showinfo("Información", "No hay datos para este producto")
            return
        
        # Crear figura
        ventana = tk.Toplevel()
        ventana.title(f"Tendencia - {producto_nombre}")
        ventana.geometry("900x500")
        
        fig = Figure(figsize=(12, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        fechas = [str(d['fecha']) for d in datos]
        cantidades = [d['cantidad'] for d in datos]
        ingresos = [d['ingresos'] for d in datos]
        
        ax.plot(fechas, cantidades, marker='o', linewidth=2, markersize=8, label='Cantidad', color='#3498db')
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cantidad Vendida', fontsize=12, fontweight='bold')
        ax.set_title(f'Tendencia de Ventas - {producto_nombre}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Rotar eje x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafica_categorias_mas_vendidas(self):
        """Muestra categorías con más ventas"""
        sql = """
            SELECT 
                c.nombre,
                SUM(dv.cantidad) as total_cantidad,
                SUM(dv.subtotal) as total_ingresos
            FROM categorias c
            JOIN productos p ON c.id = p.categoria_id
            JOIN detalle_ventas dv ON p.id = dv.producto_id
            GROUP BY c.id
            ORDER BY total_ingresos DESC
        """
        
        datos = self.bd.ejecutar_consulta(sql)
        
        if not datos:
            messagebox.showinfo("Información", "No hay datos de ventas")
            return
        
        ventana = tk.Toplevel()
        ventana.title("Categorías Más Vendidas")
        ventana.geometry("900x500")
        
        fig = Figure(figsize=(12, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        categorias = [d['nombre'] for d in datos]
        ingresos = [d['total_ingresos'] for d in datos]
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e']
        ax.bar(categorias, ingresos, color=colors[:len(categorias)], edgecolor='#2c3e50', linewidth=2)
        
        ax.set_xlabel('Categoría', fontsize=12, fontweight='bold')
        ax.set_ylabel('Ingresos ($)', fontsize=12, fontweight='bold')
        ax.set_title('Ingresos por Categoría', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Agregar valores
        for i, v in enumerate(ingresos):
            ax.text(i, v + 10, f'${v:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def grafica_tendencia_ventas_mes(self):
        """Muestra la tendencia de ventas del mes"""
        sql = """
            SELECT 
                DATE(fecha) as fecha,
                COUNT(*) as cantidad_ventas,
                SUM(total) as total_ingresos
            FROM ventas
            WHERE MONTH(fecha) = MONTH(NOW())
            AND YEAR(fecha) = YEAR(NOW())
            GROUP BY DATE(fecha)
            ORDER BY fecha
        """
        
        datos = self.bd.ejecutar_consulta(sql)
        
        if not datos:
            messagebox.showinfo("Información", "No hay datos de ventas este mes")
            return
        
        ventana = tk.Toplevel()
        ventana.title("Tendencia de Ventas del Mes")
        ventana.geometry("1000x600")
        
        fig = Figure(figsize=(13, 6), dpi=80)
        
        # Gráfica 1: Ingresos
        ax1 = fig.add_subplot(121)
        fechas = [str(d['fecha']) for d in datos]
        ingresos = [d['total_ingresos'] for d in datos]
        
        ax1.plot(fechas, ingresos, marker='o', linewidth=2.5, markersize=8, color='#27ae60', label='Ingresos')
        ax1.fill_between(range(len(fechas)), ingresos, alpha=0.3, color='#27ae60')
        ax1.set_xlabel('Fecha', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Ingresos ($)', fontsize=11, fontweight='bold')
        ax1.set_title('Ingresos Diarios', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Gráfica 2: Cantidad de ventas
        ax2 = fig.add_subplot(122)
        cantidades = [d['cantidad_ventas'] for d in datos]
        
        ax2.bar(fechas, cantidades, color='#e74c3c', edgecolor='#2c3e50', linewidth=2, alpha=0.8)
        ax2.set_xlabel('Fecha', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Cantidad de Ventas', fontsize=11, fontweight='bold')
        ax2.set_title('Cantidad de Transacciones', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Rotar eje x
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
