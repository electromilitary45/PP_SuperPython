# 🛒 Mini Super Las Botargas - Sistema de Punto de Venta

Sistema de gestión de inventario y punto de venta desarrollado en **Python** con **Tkinter** y **MySQL**.

---

## 📋 Descripción

Aplicación de escritorio para gestionar productos, registrar ventas y generar reportes de un mini super. Incluye:

- **Gestión de productos** (CRUD completo)
- **Punto de venta** con carrito y validación de stock
- **Reportes** de ventas, stock bajo, productos más/menos vendidos
- **Gráficas** de análisis de ventas con Matplotlib
- **Base de datos** MySQL con 110+ productos precargados

---

## 🚀 Instalación Rápida

### 1. **Requisitos**
- Python 3.7+
- MySQL 5.7+

### 2. **Crear Base de Datos** ⚠️ **IMPORTANTE: HACER PRIMERO**
```bash
# En MySQL ejecutar:
mysql -u root -p < database/bd.sql
```

### 3. **Instalar Dependencias**
```bash
pip install mysql-connector-python matplotlib pandas pillow
```
**Configurar el interprete de Python en su entorno si es necesario.**
```


### 4. **Configurar Credenciales**
Editar `config.py`:
```python
HOST = 'localhost'
USUARIO = 'root'
CONTRASEÑA = 'tu_contraseña'
BASE_DATOS = 'mini_super_botargas'
```

### 5. **Ejecutar**
```bash
python iniciar.py
```

---

## 📂 Estructura del Proyecto

```
PP_SuperPython/
├── database/
│   ├── bd.sql              # ⚠️ Script SQL (ejecutar primero)
│   └── conexion.py         # Clase de conexión MySQL
├── gui/
│   ├── app.py              # Ventana principal
│   ├── productos_gui.py    # Gestión de productos
│   ├── ventas_gui.py       # Punto de venta
│   ├── reportes_gui.py     # Reportes
│   └── graficas.py         # Gráficas Matplotlib
├── config.py               # Configuración BD
├── iniciar.py              # 🚀 EJECUTAR ESTE ARCHIVO
└── README.md
```

---

## 🗄️ Base de Datos

### Tablas
- **categorias**: 10 categorías (Bebidas, Snacks, Lácteos, etc.)
- **productos**: 110+ productos con precios, stock y fechas de vencimiento
- **ventas**: Registro de todas las transacciones
- **detalle_ventas**: Líneas de cada venta

### Relaciones
```
categorias (1) ──→ (N) productos
productos (1) ──→ (N) detalle_ventas
ventas (1) ──→ (N) detalle_ventas
```

---

## 💻 Funcionalidades

### Pestaña 1: Productos
- Listar productos con búsqueda en tiempo real
- Agregar, modificar y eliminar productos
- Resaltar stock bajo (fondo rojo)
- Validación de precios y stock

### Pestaña 2: Punto de Venta
- Búsqueda de productos (por nombre o ID)
- Carrito de compras visual
- Validación de stock disponible
- Métodos de pago: Efectivo, Tarjeta, Cheque
- Actualización automática de inventario

### Pestaña 3: Reportes y Gráficas
- Ventas del día
- Productos con stock bajo
- Productos más/menos vendidos
- Gráfica: Ventas por hora
- Gráfica: Tendencia producto más vendido
- Gráfica: Ingresos por categoría
- Gráfica: Tendencia del mes

---

## 🔧 Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Lenguaje | Python 3.7+ |
| Interfaz Gráfica | Tkinter (nativo) |
| Base de Datos | MySQL 5.7+ |
| Conector BD | mysql-connector-python |
| Visualización | Matplotlib |
| Análisis | Pandas |

---

## ⚙️ Arquitectura Técnica

### Capa de Datos
```python
ConexionBD(host, usuario, contraseña, bd)
├─ conectar()              # Conexión MySQL
├─ ejecutar_consulta()     # SELECT
├─ ejecutar_insertar()     # INSERT
├─ ejecutar_actualizar()   # UPDATE
└─ ejecutar_eliminar()     # DELETE
```

### Capa de Presentación
- **app.py**: Ventana principal con Notebook (3 pestañas)
- **productos_gui.py**: Frame con CRUD de productos
- **ventas_gui.py**: Frame con carrito y registro de ventas
- **reportes_gui.py**: Frame con 4 reportes + 4 gráficas

### Flujo de Venta
```
1. Buscar producto → 2. Agregar al carrito → 3. Seleccionar método de pago
→ 4. Registrar venta → 5. Actualizar stock → 6. Generar factura
```

---

## 🔒 Validaciones

- ✅ Stock disponible antes de vender
- ✅ Precio de venta > precio de compra
- ✅ Cantidades positivas
- ✅ Transacciones con rollback en caso de error
- ✅ Manejo de excepciones robusto

---

## 📝 Notas

- El script SQL **debe ejecutarse primero** para crear la base de datos
- La aplicación se abre maximizada automáticamente
- Los productos eliminados se marcan como inactivos (no se borran)
- El stock se actualiza automáticamente al registrar ventas
- Las búsquedas son en tiempo real y case-insensitive

---
