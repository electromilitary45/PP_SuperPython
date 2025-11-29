"""
GUI para Punto de Venta
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class VentasFrame(ttk.Frame):
    def __init__(self, parent, bd):
        super().__init__(parent)
        self.bd = bd
        self.carrito = []
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de ventas"""
        
        # Título
        titulo = ttk.Label(self, text="Punto de Venta", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame superior - búsqueda y agregar
        frame_superior = ttk.Frame(self)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_superior, text="🔍 Buscar Producto (nombre o ID):").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = ttk.Entry(frame_superior, width=25)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda.bind('<KeyRelease>', lambda e: self.actualizar_sugerencias())
        
        ttk.Label(frame_superior, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.entrada_cantidad = ttk.Entry(frame_superior, width=10)
        self.entrada_cantidad.pack(side=tk.LEFT, padx=5)
        self.entrada_cantidad.insert(0, "1")
        
        ttk.Button(frame_superior, text="➕ Agregar al Carrito", command=self.agregar_carrito).pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar sugerencias
        frame_sugerencias = ttk.LabelFrame(self, text="Productos Disponibles (filtrados)")
        frame_sugerencias.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        
        # Tabla de productos para seleccionar
        self.tree_productos = ttk.Treeview(
            frame_sugerencias,
            columns=('ID', 'Producto', 'Categoría', 'Precio', 'Stock'),
            height=4,
            show='headings'
        )
        
        self.tree_productos.column('ID', width=40)
        self.tree_productos.column('Producto', width=200)
        self.tree_productos.column('Categoría', width=100)
        self.tree_productos.column('Precio', width=80)
        self.tree_productos.column('Stock', width=80)
        
        self.tree_productos.heading('ID', text='ID')
        self.tree_productos.heading('Producto', text='Producto')
        self.tree_productos.heading('Categoría', text='Categoría')
        self.tree_productos.heading('Precio', text='Precio')
        self.tree_productos.heading('Stock', text='Stock')
        
        # Eventos para la tabla
        self.tree_productos.bind('<Double-1>', self.seleccionar_producto_tabla)
        
        scrollbar_prod = ttk.Scrollbar(frame_sugerencias, orient=tk.VERTICAL, command=self.tree_productos.yview)
        self.tree_productos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_prod.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame central - carrito
        ttk.Label(self, text="Carrito de Compra", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.tree_carrito = ttk.Treeview(
            self,
            columns=('Producto', 'Cantidad', 'Precio', 'Subtotal'),
            height=12,
            show='headings'
        )
        
        self.tree_carrito.column('Producto', width=250)
        self.tree_carrito.column('Cantidad', width=80)
        self.tree_carrito.column('Precio', width=80)
        self.tree_carrito.column('Subtotal', width=100)
        
        self.tree_carrito.heading('Producto', text='Producto')
        self.tree_carrito.heading('Cantidad', text='Cantidad')
        self.tree_carrito.heading('Precio', text='Precio')
        self.tree_carrito.heading('Subtotal', text='Subtotal')
        
        self.tree_carrito.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame de botones carrito
        frame_botones = ttk.Frame(self)
        frame_botones.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame_botones, text="Eliminar Seleccionado", command=self.eliminar_carrito).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="Limpiar Carrito", command=self.limpiar_carrito).pack(side=tk.LEFT, padx=2)
        
        # Frame inferior - total y botones
        frame_inferior = ttk.Frame(self)
        frame_inferior.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_inferior, text="Total:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.label_total = ttk.Label(frame_inferior, text="$0.00", font=("Arial", 12, "bold"), foreground="green")
        self.label_total.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_inferior, text="Método de Pago:").pack(side=tk.LEFT, padx=5)
        self.combo_pago = ttk.Combobox(frame_inferior, values=["Efectivo", "Tarjeta", "Cheque"], width=15, state="readonly")
        self.combo_pago.set("Efectivo")
        self.combo_pago.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_inferior, text="Registrar Venta", command=self.registrar_venta).pack(side=tk.LEFT, padx=5)
        
        # Cargar productos iniciales
        self.cargar_todos_productos()
    
    def agregar_carrito(self):
        """Agrega un producto al carrito"""
        try:
            nombre_busqueda = self.entrada_busqueda.get().strip()
            cantidad = int(self.entrada_cantidad.get())
            
            if not nombre_busqueda or cantidad <= 0:
                messagebox.showwarning("Aviso", "Ingresa nombre y cantidad válidos")
                return
            
            # Buscar producto
            sql = """
                SELECT p.id, p.nombre, p.precio_venta, p.stock, c.nombre as categoria
                FROM productos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.activo = TRUE AND (p.nombre LIKE %s OR p.id = %s)
                LIMIT 1
            """
            
            productos = self.bd.ejecutar_consulta(sql, (f"%{nombre_busqueda}%", nombre_busqueda))
            
            if not productos:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            producto = productos[0]
            
            # Validar stock
            if producto['stock'] < cantidad:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
                return
            
            # Agregar al carrito
            subtotal = producto['precio_venta'] * cantidad
            self.carrito.append({
                'id': producto['id'],
                'nombre': producto['nombre'],
                'cantidad': cantidad,
                'precio': producto['precio_venta'],
                'subtotal': subtotal
            })
            
            self.actualizar_carrito()
            self.entrada_busqueda.delete(0, tk.END)
            self.entrada_cantidad.delete(0, tk.END)
            self.entrada_cantidad.insert(0, "1")
            messagebox.showinfo("Éxito", f"{producto['nombre']} agregado al carrito")
        
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
    
    def actualizar_carrito(self):
        """Actualiza la visualización del carrito"""
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        total = 0
        for item in self.carrito:
            self.tree_carrito.insert('', tk.END, values=(
                item['nombre'],
                item['cantidad'],
                f"${item['precio']:.2f}",
                f"${item['subtotal']:.2f}"
            ))
            total += item['subtotal']
        
        self.label_total.config(text=f"${total:.2f}")
    
    def eliminar_carrito(self):
        """Elimina un producto del carrito"""
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return
        
        index = self.tree_carrito.index(seleccion[0])
        self.carrito.pop(index)
        self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpia todo el carrito"""
        self.carrito = []
        self.actualizar_carrito()
    
    def registrar_venta(self):
        """Registra la venta en la BD"""
        if not self.carrito:
            messagebox.showwarning("Aviso", "El carrito está vacío")
            return
        
        # Calcular total
        total = sum(item['subtotal'] for item in self.carrito)
        
        try:
            # Registrar venta
            fecha = datetime.now().date()
            hora = datetime.now().time()
            metodo_pago = self.combo_pago.get()
            
            sql_venta = "INSERT INTO ventas (fecha, hora, total, metodo_pago) VALUES (%s, %s, %s, %s)"
            venta_id = self.bd.ejecutar_insertar(sql_venta, (fecha, hora, total, metodo_pago))
            
            if venta_id == 0:
                messagebox.showerror("Error", "No se pudo registrar la venta")
                return
            
            # Registrar detalles y actualizar stock
            for item in self.carrito:
                # Insertar detalle
                sql_detalle = """
                    INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.bd.ejecutar_insertar(sql_detalle, 
                    (venta_id, item['id'], item['cantidad'], item['precio'], item['subtotal']))
                
                # Actualizar stock
                sql_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
                self.bd.ejecutar_actualizar(sql_stock, (item['cantidad'], item['id']))
            
            messagebox.showinfo("Éxito", f"Venta registrada. Factura #{venta_id}\nTotal: ${total:.2f}")
            self.limpiar_carrito()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")
    
    # ===== NUEVOS MÉTODOS PARA BÚSQUEDA EN TIEMPO REAL =====
    
    def cargar_todos_productos(self):
        """Carga todos los productos en la tabla de sugerencias"""
        sql = """
            SELECT 
                p.id,
                p.nombre,
                c.nombre as categoria,
                p.precio_venta,
                p.stock
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY p.nombre
        """
        
        self.todos_productos = self.bd.ejecutar_consulta(sql) or []
        self.actualizar_sugerencias()
    
    def actualizar_sugerencias(self):
        """Actualiza la tabla de productos según la búsqueda en tiempo real"""
        # Limpiar tabla
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Obtener término de búsqueda
        termino = self.entrada_busqueda.get().lower().strip()
        
        # Si no hay término, mostrar todos
        if not termino:
            productos_filtrados = self.todos_productos
        else:
            # Filtrar por nombre o ID
            productos_filtrados = [
                p for p in self.todos_productos
                if termino in p['nombre'].lower() or termino in str(p['id'])
            ]
        
        # Insertar productos filtrados
        for prod in productos_filtrados[:20]:  # Limitar a 20 resultados
            tag = 'stock_bajo' if prod['stock'] <= 5 else ''
            self.tree_productos.insert('', tk.END, values=(
                prod['id'],
                prod['nombre'],
                prod['categoria'],
                f"${prod['precio_venta']:.2f}",
                prod['stock']
            ), tags=(tag,))
        
        # Configurar colores
        self.tree_productos.tag_configure('stock_bajo', background='#ffcccc')
    
    def seleccionar_producto_tabla(self, event):
        """Selecciona un producto de la tabla con doble click"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        
        item = self.tree_productos.item(seleccion[0])
        valores = item['values']
        
        # Obtener datos del producto
        producto_id = valores[0]
        producto_nombre = valores[1]
        
        # Llenar el campo de búsqueda y cantidad
        self.entrada_busqueda.delete(0, tk.END)
        self.entrada_busqueda.insert(0, producto_nombre)
        
        self.entrada_cantidad.delete(0, tk.END)
        self.entrada_cantidad.insert(0, "1")
        
        # Agregar al carrito automáticamente
        self.agregar_carrito()
