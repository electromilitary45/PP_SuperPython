"""
MINI SUPER LAS BOTARGAS - PUNTO DE VENTA
Proyecto Final - Programación para el Análisis de Datos
"""

from database.conexion import ConexionBD
from config import HOST, USUARIO, CONTRASEÑA, BASE_DATOS
import os
from datetime import datetime


class SistemaVentas:
    def __init__(self):
        # Configuración de base de datos
        self.bd = ConexionBD(
            host=HOST,
            usuario=USUARIO,
            contraseña=CONTRASEÑA,
            base_datos=BASE_DATOS
        )
        self.conexion = None
    
    def conectar(self):
        """Conecta a la base de datos"""
        self.conexion = self.bd.conectar()
        if self.conexion is None:
            print("\n✗ No se pudo conectar a la base de datos")
            print("Verifica tu usuario y contraseña de MySQL")
            return False
        return True
    
    def desconectar(self):
        """Desconecta de la base de datos"""
        self.bd.desconectar()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_encabezado(self):
        """Muestra el encabezado del sistema"""
        print("\n")
        print("=" * 60)
        print("         MINI SUPER LAS BOTARGAS - PUNTO DE VENTA")
        print("=" * 60)
        print()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("MENÚ PRINCIPAL\n")
        print("1. Gestión de Productos")
        print("2. Registrar Venta")
        print("3. Reportes y Análisis")
        print("4. Salir\n")
        
        return input("Selecciona una opción (1-4): ").strip()
    
    def mostrar_menu_productos(self):
        """Muestra el menú de gestión de productos"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("GESTIÓN DE PRODUCTOS\n")
        print("1. Agregar producto")
        print("2. Modificar producto")
        print("3. Eliminar producto")
        print("4. Listar productos")
        print("5. Ver producto por categoría")
        print("6. Volver al menú principal\n")
        
        return input("Selecciona una opción (1-6): ").strip()
    
    def mostrar_menu_reportes(self):
        """Muestra el menú de reportes"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("REPORTES Y ANÁLISIS\n")
        print("1. Reporte de ventas del día")
        print("2. Reporte de productos próximos a agotarse")
        print("3. Reporte de productos más vendidos")
        print("4. Reporte de productos menos vendidos")
        print("5. Gráfica de tendencia del producto más vendido")
        print("6. Gráfica de ventas por hora")
        print("7. Volver al menú principal\n")
        
        return input("Selecciona una opción (1-7): ").strip()
    
    # ===== MÉTODOS DE PRODUCTOS =====
    
    def agregar_producto(self):
        """Agrega un nuevo producto al inventario"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("AGREGAR NUEVO PRODUCTO\n")
        
        # Obtener categorías
        categorias = self.bd.ejecutar_consulta("SELECT id, nombre FROM categorias")
        if not categorias:
            print("✗ No hay categorías disponibles")
            input("Presiona Enter para continuar...")
            return
        
        print("Categorías disponibles:")
        for cat in categorias:
            print(f"  {cat['id']}. {cat['nombre']}")
        
        try:
            categoria_id = int(input("\nSelecciona categoría (ID): ").strip())
            nombre = input("Nombre del producto: ").strip()
            precio_compra = float(input("Precio de compra: "))
            precio_venta = float(input("Precio de venta: "))
            stock = int(input("Stock inicial: "))
            stock_minimo = int(input("Stock mínimo: "))
            fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD) [opcional, presiona Enter]: ").strip()
            
            # Validaciones
            if not nombre:
                print("✗ El nombre del producto no puede estar vacío")
                input("Presiona Enter para continuar...")
                return
            
            if precio_venta <= precio_compra:
                print("✗ El precio de venta debe ser mayor al precio de compra")
                input("Presiona Enter para continuar...")
                return
            
            # Preparar SQL
            sql = """
                INSERT INTO productos 
                (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            parametros = (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, 
                         fecha_vencimiento if fecha_vencimiento else None)
            
            id_producto = self.bd.ejecutar_insertar(sql, parametros)
            
            if id_producto > 0:
                print(f"\n✓ Producto '{nombre}' agregado exitosamente con ID: {id_producto}")
            else:
                print("\n✗ Error al agregar el producto")
        
        except ValueError:
            print("\n✗ Error: Ingresa valores válidos")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presiona Enter para continuar...")
    
    def listar_productos(self):
        """Lista todos los productos del inventario"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("LISTADO DE PRODUCTOS\n")
        
        sql = """
            SELECT 
                p.id, 
                p.nombre, 
                c.nombre as categoria,
                p.precio_compra,
                p.precio_venta,
                p.stock,
                p.stock_minimo,
                p.fecha_vencimiento
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY c.nombre, p.nombre
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        if not productos:
            print("✗ No hay productos disponibles")
            input("Presiona Enter para continuar...")
            return
        
        print(f"{'ID':<5} {'Producto':<30} {'Categoría':<20} {'Stock':<6} {'Precio':<8}")
        print("-" * 75)
        
        for prod in productos:
            print(f"{prod['id']:<5} {prod['nombre']:<30} {prod['categoria']:<20} {prod['stock']:<6} ${prod['precio_venta']:<7.2f}")
        
        print(f"\nTotal de productos: {len(productos)}")
        input("Presiona Enter para continuar...")
    
    def modificar_producto(self):
        """Modifica un producto existente"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("MODIFICAR PRODUCTO\n")
        
        try:
            producto_id = int(input("ID del producto a modificar: ").strip())
            
            # Verificar que existe
            sql = "SELECT * FROM productos WHERE id = %s"
            producto = self.bd.ejecutar_consulta(sql, (producto_id,))
            
            if not producto:
                print("✗ Producto no encontrado")
                input("Presiona Enter para continuar...")
                return
            
            print(f"\nProducto actual: {producto[0]['nombre']}")
            print("¿Qué deseas modificar?")
            print("1. Nombre")
            print("2. Precio de compra")
            print("3. Precio de venta")
            print("4. Stock")
            print("5. Stock mínimo")
            print("6. Volver\n")
            
            opcion = input("Selecciona opción: ").strip()
            
            if opcion == "6":
                return
            
            nuevovalor = input("Nuevo valor: ").strip()
            
            campos = {
                "1": "nombre",
                "2": "precio_compra",
                "3": "precio_venta",
                "4": "stock",
                "5": "stock_minimo"
            }
            
            if opcion in campos:
                sql_update = f"UPDATE productos SET {campos[opcion]} = %s WHERE id = %s"
                resultado = self.bd.ejecutar_actualizar(sql_update, (nuevovalor, producto_id))
                
                if resultado > 0:
                    print("✓ Producto actualizado exitosamente")
                else:
                    print("✗ Error al actualizar el producto")
            else:
                print("✗ Opción no válida")
        
        except ValueError:
            print("✗ Error: Ingresa un ID válido")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        input("Presiona Enter para continuar...")
    
    def eliminar_producto(self):
        """Elimina un producto (marca como inactivo)"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("ELIMINAR PRODUCTO\n")
        
        try:
            producto_id = int(input("ID del producto a eliminar: ").strip())
            
            # Verificar que existe
            sql = "SELECT nombre FROM productos WHERE id = %s"
            producto = self.bd.ejecutar_consulta(sql, (producto_id,))
            
            if not producto:
                print("✗ Producto no encontrado")
                input("Presiona Enter para continuar...")
                return
            
            confirmacion = input(f"¿Estás seguro de eliminar '{producto[0]['nombre']}'? (s/n): ").strip().lower()
            
            if confirmacion == 's':
                sql_delete = "UPDATE productos SET activo = FALSE WHERE id = %s"
                resultado = self.bd.ejecutar_actualizar(sql_delete, (producto_id,))
                
                if resultado > 0:
                    print("✓ Producto eliminado exitosamente")
                else:
                    print("✗ Error al eliminar el producto")
            else:
                print("Operación cancelada")
        
        except ValueError:
            print("✗ Error: Ingresa un ID válido")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        input("Presiona Enter para continuar...")
    
    # ===== MÉTODOS DE VENTAS =====
    
    def registrar_venta(self):
        """Registra una nueva venta"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("REGISTRAR NUEVA VENTA\n")
        print("(Escribe 'listo' cuando termines de agregar productos)\n")
        
        productos_venta = []
        total = 0
        
        while True:
            try:
                producto_id = input("ID del producto (o 'listo'): ").strip().lower()
                
                if producto_id == 'listo':
                    if not productos_venta:
                        print("✗ Debes agregar al menos un producto")
                        continue
                    break
                
                producto_id = int(producto_id)
                cantidad = int(input("Cantidad: ").strip())
                
                # Obtener producto y validar stock
                sql = "SELECT * FROM productos WHERE id = %s AND activo = TRUE"
                producto = self.bd.ejecutar_consulta(sql, (producto_id,))
                
                if not producto:
                    print("✗ Producto no encontrado")
                    continue
                
                prod = producto[0]
                
                if prod['stock'] < cantidad:
                    print(f"✗ Stock insuficiente. Disponible: {prod['stock']}")
                    continue
                
                subtotal = prod['precio_venta'] * cantidad
                total += subtotal
                
                productos_venta.append({
                    'producto_id': producto_id,
                    'nombre': prod['nombre'],
                    'cantidad': cantidad,
                    'precio_unitario': prod['precio_venta'],
                    'subtotal': subtotal
                })
                
                print(f"✓ {prod['nombre']} agregado a la venta")
            
            except ValueError:
                print("✗ Error: Ingresa valores válidos")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE VENTA\n")
        
        for item in productos_venta:
            print(f"{item['nombre']}: {item['cantidad']} x ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f}")
        
        print("-" * 60)
        print(f"TOTAL: ${total:.2f}")
        print("=" * 60)
        
        metodo_pago = input("\nMétodo de pago (Efectivo/Tarjeta): ").strip() or "Efectivo"
        confirmacion = input("¿Confirmar venta? (s/n): ").strip().lower()
        
        if confirmacion != 's':
            print("✗ Venta cancelada")
            input("Presiona Enter para continuar...")
            return
        
        try:
            # Registrar venta
            fecha = datetime.now().date()
            hora = datetime.now().time().strftime('%H:%M:%S')
            
            sql_venta = "INSERT INTO ventas (fecha, hora, total, metodo_pago) VALUES (%s, %s, %s, %s)"
            venta_id = self.bd.ejecutar_insertar(sql_venta, (fecha, hora, total, metodo_pago))
            
            if venta_id == 0:
                print("✗ Error al registrar la venta")
                input("Presiona Enter para continuar...")
                return
            
            # Registrar detalles y actualizar stock
            for item in productos_venta:
                # Insertar detalle
                sql_detalle = """
                    INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.bd.ejecutar_insertar(sql_detalle, 
                    (venta_id, item['producto_id'], item['cantidad'], item['precio_unitario'], item['subtotal']))
                
                # Actualizar stock
                sql_stock = "UPDATE productos SET stock = stock - %s WHERE id = %s"
                self.bd.ejecutar_actualizar(sql_stock, (item['cantidad'], item['producto_id']))
            
            print(f"\n✓ Venta registrada exitosamente. Factura #{venta_id}")
        
        except Exception as e:
            print(f"✗ Error al registrar la venta: {e}")
        
        input("Presiona Enter para continuar...")
    
    # ===== MÉTODOS DE REPORTES =====
    
    def reporte_ventas_dia(self):
        """Muestra el reporte de ventas del día"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("REPORTE DE VENTAS DEL DÍA\n")
        
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
        
        if not ventas:
            print(f"No hay ventas registradas para {fecha}")
            input("Presiona Enter para continuar...")
            return
        
        print(f"Fecha: {fecha}\n")
        print(f"{'Factura':<8} {'Hora':<10} {'Total':<10} {'Método':<10} {'Productos':<10}")
        print("-" * 50)
        
        total_ventas = 0
        for venta in ventas:
            print(f"{venta['id']:<8} {str(venta['hora']):<10} ${venta['total']:<9.2f} {venta['metodo_pago']:<10} {venta['cantidad_productos']:<10}")
            total_ventas += venta['total']
        
        print("-" * 50)
        print(f"TOTAL DEL DÍA: ${total_ventas:.2f}")
        print(f"CANTIDAD DE VENTAS: {len(ventas)}")
        
        input("Presiona Enter para continuar...")
    
    def reporte_stock_bajo(self):
        """Muestra productos próximos a agotarse"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("PRODUCTOS PRÓXIMOS A AGOTARSE\n")
        
        sql = """
            SELECT 
                p.id,
                p.nombre,
                c.nombre as categoria,
                p.stock,
                p.stock_minimo,
                p.fecha_vencimiento
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock <= p.stock_minimo AND p.activo = TRUE
            ORDER BY p.stock ASC
        """
        
        productos = self.bd.ejecutar_consulta(sql)
        
        if not productos:
            print("✓ No hay productos con stock bajo")
            input("Presiona Enter para continuar...")
            return
        
        print(f"{'ID':<5} {'Producto':<25} {'Stock':<8} {'Mínimo':<8} {'Vencimiento':<15}")
        print("-" * 65)
        
        for prod in productos:
            vencimiento = prod['fecha_vencimiento'] if prod['fecha_vencimiento'] else "N/A"
            print(f"{prod['id']:<5} {prod['nombre']:<25} {prod['stock']:<8} {prod['stock_minimo']:<8} {str(vencimiento):<15}")
        
        print(f"\nTotal de productos con stock bajo: {len(productos)}")
        
        input("Presiona Enter para continuar...")
    
    # ===== MENÚ PRINCIPAL =====
    
    def ejecutar(self):
        """Ejecuta el sistema principal"""
        if not self.conectar():
            return
        
        try:
            while True:
                opcion = self.mostrar_menu_principal()
                
                if opcion == "1":
                    while True:
                        opcion_prod = self.mostrar_menu_productos()
                        
                        if opcion_prod == "1":
                            self.agregar_producto()
                        elif opcion_prod == "2":
                            self.modificar_producto()
                        elif opcion_prod == "3":
                            self.eliminar_producto()
                        elif opcion_prod == "4":
                            self.listar_productos()
                        elif opcion_prod == "6":
                            break
                        else:
                            print("✗ Opción no válida")
                            input("Presiona Enter para continuar...")
                
                elif opcion == "2":
                    self.registrar_venta()
                
                elif opcion == "3":
                    while True:
                        opcion_rep = self.mostrar_menu_reportes()
                        
                        if opcion_rep == "1":
                            self.reporte_ventas_dia()
                        elif opcion_rep == "2":
                            self.reporte_stock_bajo()
                        elif opcion_rep == "7":
                            break
                        else:
                            print("✗ Opción no válida")
                            input("Presiona Enter para continuar...")
                
                elif opcion == "4":
                    print("\n✓ ¡Hasta luego!")
                    break
                
                else:
                    print("✗ Opción no válida")
                    input("Presiona Enter para continuar...")
        
        finally:
            self.desconectar()


if __name__ == "__main__":
    sistema = SistemaVentas()
    sistema.ejecutar()
