"""
GUI para gestión de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta


class ProductosFrame(ttk.Frame):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.bd = bd
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de productos"""
        
        # Título
        titulo = ttk.Label(self, text="Gestión de Productos", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame de botones
        frame_botones = ttk.Frame(self)
        frame_botones.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame_botones, text="➕ Agregar", command=self.agregar_producto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️  Modificar", command=self.modificar_producto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️  Eliminar", command=self.eliminar_producto).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Recargar", command=self.cargar_productos).pack(side=tk.LEFT, padx=2)
        
        # Frame de búsqueda
        frame_busqueda = ttk.Frame(self)
        frame_busqueda.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = ttk.Entry(frame_busqueda, width=30)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda.bind('<KeyRelease>', lambda e: self.filtrar_productos())
        
        # Tabla de productos
        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'Producto', 'Categoría', 'Precio', 'Stock', 'Mínimo'),
            height=15,
            show='headings'
        )
        
        # Definir encabezados
        self.tree.column('ID', width=40)
        self.tree.column('Producto', width=200)
        self.tree.column('Categoría', width=120)
        self.tree.column('Precio', width=80)
        self.tree.column('Stock', width=80)
        self.tree.column('Mínimo', width=80)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Producto', text='Producto')
        self.tree.heading('Categoría', text='Categoría')
        self.tree.heading('Precio', text='Precio')
        self.tree.heading('Stock', text='Stock')
        self.tree.heading('Mínimo', text='Mínimo')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos iniciales
        self.cargar_productos()
    
    def cargar_productos(self):
        """Carga los productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Consultar productos
        sql = """
            SELECT 
                p.id,
                p.nombre,
                c.nombre as categoria,
                p.precio_venta,
                p.stock,
                p.stock_minimo
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY c.nombre, p.nombre
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        if productos:
            for prod in productos:
                valores = (
                    prod['id'],
                    prod['nombre'],
                    prod['categoria'],
                    f"${prod['precio_venta']:.2f}",
                    prod['stock'],
                    prod['stock_minimo']
                )
                # Colorear fila si stock es bajo
                tag = 'stock_bajo' if prod['stock'] <= prod['stock_minimo'] else ''
                self.tree.insert('', tk.END, values=valores, tags=(tag,))
        
        # Configurar colores
        self.tree.tag_configure('stock_bajo', background='#ffcccc')
    
    def filtrar_productos(self):
        """Filtra productos por búsqueda"""
        termino = self.entrada_busqueda.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sql = """
            SELECT 
                p.id,
                p.nombre,
                c.nombre as categoria,
                p.precio_venta,
                p.stock,
                p.stock_minimo
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY c.nombre, p.nombre
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        if productos:
            for prod in productos:
                if termino in prod['nombre'].lower() or termino in prod['categoria'].lower():
                    valores = (
                        prod['id'],
                        prod['nombre'],
                        prod['categoria'],
                        f"${prod['precio_venta']:.2f}",
                        prod['stock'],
                        prod['stock_minimo']
                    )
                    tag = 'stock_bajo' if prod['stock'] <= prod['stock_minimo'] else ''
                    self.tree.insert('', tk.END, values=valores, tags=(tag,))
    
    def agregar_producto(self):
        """Abre diálogo para agregar producto"""
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Producto")
        ventana.geometry("400x400")
        
        # Obtener categorías
        categorias = self.bd.ejecutar_consulta("SELECT id, nombre FROM categorias ORDER BY nombre")
        cat_dict = {cat['nombre']: cat['id'] for cat in categorias} if categorias else {}
        
        # Formulario
        ttk.Label(ventana, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_nombre = ttk.Entry(ventana, width=30)
        entrada_nombre.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Categoría:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        categoria_var = tk.StringVar()
        combo_cat = ttk.Combobox(ventana, textvariable=categoria_var, values=list(cat_dict.keys()), width=28)
        combo_cat.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Precio Compra:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_compra = ttk.Entry(ventana, width=30)
        entrada_compra.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Precio Venta:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_venta = ttk.Entry(ventana, width=30)
        entrada_venta.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Stock:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_stock = ttk.Entry(ventana, width=30)
        entrada_stock.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Stock Mínimo:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_minimo = ttk.Entry(ventana, width=30)
        entrada_minimo.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Vencimiento (YYYY-MM-DD):").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_vencimiento = ttk.Entry(ventana, width=30)
        entrada_vencimiento.grid(row=6, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                nombre = entrada_nombre.get().strip()
                categoria = categoria_var.get()
                precio_compra = float(entrada_compra.get())
                precio_venta = float(entrada_venta.get())
                stock = int(entrada_stock.get())
                stock_minimo = int(entrada_minimo.get())
                vencimiento = entrada_vencimiento.get() or None
                
                if not nombre or not categoria:
                    messagebox.showerror("Error", "Completa todos los campos")
                    return
                
                if precio_venta <= precio_compra:
                    messagebox.showerror("Error", "Precio venta debe ser > precio compra")
                    return
                
                categoria_id = cat_dict[categoria]
                sql = """
                    INSERT INTO productos 
                    (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                resultado = self.bd.ejecutar_insertar(
                    sql,
                    (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, vencimiento)
                )
                
                if resultado > 0:
                    messagebox.showinfo("Éxito", "Producto agregado")
                    self.cargar_productos()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo agregar")
            
            except ValueError:
                messagebox.showerror("Error", "Verifica los valores ingresados")
        
        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=7, column=0, columnspan=2, pady=20)
    
    def modificar_producto(self):
        """Modifica el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return
        
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        
        sql = "SELECT * FROM productos WHERE id = %s"
        producto = self.bd.ejecutar_consulta(sql, (producto_id,))
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        prod = producto[0]
        
        ventana = tk.Toplevel(self)
        ventana.title("Modificar Producto")
        ventana.geometry("400x200")
        
        ttk.Label(ventana, text="Stock:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_stock = ttk.Entry(ventana, width=30)
        entrada_stock.insert(0, str(prod['stock']))
        entrada_stock.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(ventana, text="Precio Venta:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        entrada_precio = ttk.Entry(ventana, width=30)
        entrada_precio.insert(0, str(prod['precio_venta']))
        entrada_precio.grid(row=1, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                stock = int(entrada_stock.get())
                precio = float(entrada_precio.get())
                
                sql = "UPDATE productos SET stock = %s, precio_venta = %s WHERE id = %s"
                self.bd.ejecutar_actualizar(sql, (stock, precio, producto_id))
                messagebox.showinfo("Éxito", "Producto actualizado")
                self.cargar_productos()
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Valores inválidos")
        
        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=2, column=0, columnspan=2, pady=20)
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return
        
        item = self.tree.item(seleccion[0])
        producto_id = item['values'][0]
        producto_nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{producto_nombre}'?"):
            sql = "UPDATE productos SET activo = FALSE WHERE id = %s"
            self.bd.ejecutar_actualizar(sql, (producto_id,))
            messagebox.showinfo("Éxito", "Producto eliminado")
            self.cargar_productos()
