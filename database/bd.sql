-- =====================================================
-- MINI SUPER LAS BOTARGAS - SCRIPT DE BASE DE DATOS
-- =====================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS mini_super_botargas;
USE mini_super_botargas;

-- =====================================================
-- TABLA: CATEGORIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA: PRODUCTOS
-- =====================================================
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria_id INT NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    stock_minimo INT DEFAULT 5,
    fecha_vencimiento DATE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria_id),
    INDEX idx_stock (stock)
);

-- =====================================================
-- TABLA: VENTAS
-- =====================================================
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50) DEFAULT 'Efectivo',
    estado VARCHAR(20) DEFAULT 'Completada',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fecha (fecha),
    INDEX idx_hora (hora)
);

-- =====================================================
-- TABLA: DETALLE_VENTAS
-- =====================================================
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    INDEX idx_venta (venta_id),
    INDEX idx_producto (producto_id)
);

-- =====================================================
-- INSERTAR CATEGORÍAS INICIALES
-- =====================================================
INSERT INTO categorias (nombre, descripcion) VALUES
('Bebidas', 'Refrescos, jugos, agua'),
('Snacks', 'Papas, galletas, frutos secos'),
('Lácteos', 'Leche, queso, yogur'),
('Panadería', 'Pan, pasteles, arepas'),
('Productos de Aseo', 'Jabón, shampoo, desinfectantes'),
('Alimentos Enlatados', 'Conservas, atún, frijoles'),
('Condimentos', 'Sal, aceite, salsas'),
('Dulces', 'Chocolates, caramelos, postres'),
('Frutas y Verduras', 'Frutas y vegetales frescos'),
('Carne y Embutidos', 'Carnes, jamón, salchichas');

-- =====================================================
-- INSERTAR PRODUCTOS DE EJEMPLO (100+)
-- =====================================================

-- Bebidas (10 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Coca Cola 2L', 1, 2.50, 3.50, 45, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Sprite 2L', 1, 2.30, 3.20, 38, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Jugo Tang Naranja', 1, 1.50, 2.20, 52, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Agua embotellada 6L', 1, 1.20, 1.80, 60, 15, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Gaseosa Kola Real 2L', 1, 2.00, 2.80, 35, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Jugo Tropicana Naranja', 1, 2.80, 3.80, 28, 8, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Cerveza Modelo 12oz', 1, 1.80, 2.50, 40, 15, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Refresco Inca Kola', 1, 2.10, 2.90, 33, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Bebida Energética Red Bull', 1, 2.00, 3.50, 22, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Agua con Gas San Pellegrino', 1, 1.50, 2.50, 18, 5, DATE_ADD(CURDATE(), INTERVAL 180 DAY));

-- Snacks (15 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Papas Lays Natural', 2, 0.80, 1.50, 70, 15, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Papas Lays BBQ', 2, 0.85, 1.60, 65, 15, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Doritos Nacho', 2, 0.90, 1.70, 55, 12, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Galleta Oreo', 2, 1.20, 2.00, 48, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Galleta Marías', 2, 0.50, 1.00, 80, 20, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Cacahuetes Salados', 2, 1.50, 2.50, 35, 8, DATE_ADD(CURDATE(), INTERVAL 90 DAY)),
('Almendras Naturales', 2, 3.00, 4.50, 20, 5, DATE_ADD(CURDATE(), INTERVAL 90 DAY)),
('Granola con Pasas', 2, 2.20, 3.50, 28, 8, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Maíz Tostado', 2, 0.60, 1.20, 42, 10, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Frutos Secos Mix', 2, 2.50, 4.00, 25, 5, DATE_ADD(CURDATE(), INTERVAL 90 DAY)),
('Chizitos', 2, 0.75, 1.40, 58, 15, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Takis Fuego', 2, 0.95, 1.80, 45, 12, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Platanitos', 2, 0.85, 1.60, 52, 12, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Tortrix', 2, 0.80, 1.50, 60, 15, DATE_ADD(CURDATE(), INTERVAL 120 DAY)),
('Cheetos Puff', 2, 0.90, 1.70, 50, 12, DATE_ADD(CURDATE(), INTERVAL 120 DAY));

-- Lácteos (10 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Leche Fresca 1L', 3, 1.00, 1.50, 75, 20, DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Queso Fresco', 3, 4.00, 6.50, 30, 8, DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
('Yogur Natural 1L', 3, 1.50, 2.25, 45, 12, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Mantequilla 250g', 3, 2.50, 4.00, 25, 8, DATE_ADD(CURDATE(), INTERVAL 30 DAY)),
('Crema de Leche', 3, 1.80, 2.80, 20, 5, DATE_ADD(CURDATE(), INTERVAL 20 DAY)),
('Queso Mozzarella', 3, 3.50, 5.50, 22, 5, DATE_ADD(CURDATE(), INTERVAL 20 DAY)),
('Yogur Frutal Fresa', 3, 1.20, 1.80, 50, 15, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Leche Descremada 1L', 3, 0.95, 1.45, 40, 12, DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Queso Cheddar', 3, 4.50, 7.00, 18, 5, DATE_ADD(CURDATE(), INTERVAL 30 DAY)),
('Kumis Sabor Chocolate', 3, 1.50, 2.25, 35, 10, DATE_ADD(CURDATE(), INTERVAL 10 DAY));

-- Panadería (12 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Pan Integral 500g', 4, 1.20, 2.00, 60, 15, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Pan Blanco 500g', 4, 1.00, 1.80, 80, 20, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Arepa Harina 1kg', 4, 2.00, 3.50, 45, 10, DATE_ADD(CURDATE(), INTERVAL 30 DAY)),
('Croissant Chocolate', 4, 0.80, 1.50, 35, 10, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Donas Azucaradas', 4, 0.60, 1.20, 50, 15, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Galleta de Soda', 4, 0.40, 0.80, 100, 25, DATE_ADD(CURDATE(), INTERVAL 30 DAY)),
('Biscocho de Vainilla', 4, 1.50, 2.50, 25, 8, DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
('Tarta de Manzana', 4, 2.50, 4.50, 15, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Pan de Ajo 300g', 4, 1.80, 3.00, 20, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Muffin Blueberry', 4, 1.20, 2.00, 30, 8, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Baguette Francesa', 4, 1.50, 2.80, 22, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Pan de Tres Puntas', 4, 0.90, 1.60, 40, 10, DATE_ADD(CURDATE(), INTERVAL 2 DAY));

-- Productos de Aseo (12 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Jabón Líquido 500ml', 5, 1.50, 2.50, 55, 12, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Shampoo Neutrogena 400ml', 5, 3.00, 5.00, 35, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Desinfectante Lysol 500ml', 5, 2.00, 3.50, 40, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Detergente Ariel 500g', 5, 2.50, 4.00, 50, 15, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Pasta Dental Colgate 90g', 5, 1.00, 1.80, 60, 15, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Papel Higiénico Rollo x4', 5, 2.00, 3.50, 70, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Toallitas Desmaquillantes', 5, 1.80, 3.00, 25, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Acondicionador Pantene 400ml', 5, 3.50, 5.50, 30, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Jabón de Baño Dove', 5, 1.20, 2.00, 65, 15, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Limpia Pisos Fabuloso 500ml', 5, 1.50, 2.50, 45, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Servilletas Paquete x100', 5, 0.80, 1.50, 80, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Cloro Clorox 1L', 5, 1.50, 2.50, 35, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY));

-- Alimentos Enlatados (12 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Atún en Agua 170g', 6, 1.20, 2.00, 85, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Frijoles en Lata 400g', 6, 0.80, 1.50, 75, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Chiles Poblanos 400g', 6, 1.50, 2.50, 30, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Arvejas en Lata 300g', 6, 0.90, 1.60, 50, 12, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Maíz en Lata 400g', 6, 0.85, 1.50, 60, 15, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Salsa Tomate 400g', 6, 0.70, 1.30, 70, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Sardinas en Lata 125g', 6, 1.50, 2.50, 40, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Leche Condensada 395g', 6, 1.80, 3.00, 35, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Piña en Lata 400g', 6, 1.20, 2.00, 25, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Duraznos en Lata 420g', 6, 1.30, 2.20, 28, 7, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Champiñones 200g', 6, 1.50, 2.50, 20, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Tomates Pelados 400g', 6, 0.95, 1.60, 45, 12, DATE_ADD(CURDATE(), INTERVAL 365 DAY));

-- Condimentos (10 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Sal Refinada 1kg', 7, 0.50, 1.00, 80, 20, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Aceite Vegetal 1L', 7, 2.50, 4.00, 45, 10, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Vinagre Blanco 500ml', 7, 1.00, 1.80, 35, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Mostaza Amarilla 200g', 7, 1.20, 2.00, 30, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Mayonesa Helmans 500g', 7, 2.00, 3.50, 40, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Salsa Sriracha 200ml', 7, 1.80, 3.00, 22, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Pimienta Negra 100g', 7, 2.50, 4.00, 15, 3, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Orégano Seco 50g', 7, 1.50, 2.50, 18, 3, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Ajo Molido 100g', 7, 1.80, 3.00, 20, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Salsa de Soya 500ml', 7, 1.50, 2.50, 28, 8, DATE_ADD(CURDATE(), INTERVAL 365 DAY));

-- Dulces (15 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Chocolate Nestlé 100g', 8, 0.80, 1.50, 70, 15, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Caramelos Varios', 8, 1.00, 1.80, 60, 15, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Chicle Orbit', 8, 0.30, 0.70, 100, 25, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Goma de Oso Haribo', 8, 1.20, 2.00, 45, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Chocolate Ferrero Rocher', 8, 2.50, 4.00, 30, 8, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Dulce de Leche 400g', 8, 1.80, 3.00, 35, 8, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Bombones Surtidos', 8, 3.50, 5.50, 25, 5, DATE_ADD(CURDATE(), INTERVAL 90 DAY)),
('Mentas Cereza', 8, 0.40, 0.90, 80, 20, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Toffee Halls', 8, 0.50, 1.00, 70, 15, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Chocolate Amargo 85%', 8, 1.50, 2.50, 35, 8, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Caramelo Masticable', 8, 0.60, 1.20, 55, 12, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Chocolate Blanco', 8, 1.00, 1.80, 40, 10, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Malvaviscos Grandes', 8, 1.50, 2.50, 25, 5, DATE_ADD(CURDATE(), INTERVAL 180 DAY)),
('Miel Pura 500ml', 8, 3.00, 5.00, 20, 5, DATE_ADD(CURDATE(), INTERVAL 365 DAY)),
('Dulce Casero', 8, 2.50, 4.00, 30, 8, DATE_ADD(CURDATE(), INTERVAL 90 DAY));

-- Frutas y Verduras (15 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Manzanas Rojas kg', 9, 1.50, 2.50, 50, 12, DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Plátanos kg', 9, 0.80, 1.50, 80, 20, DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
('Naranjas kg', 9, 1.20, 2.00, 60, 15, DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Papaya kg', 9, 1.50, 2.50, 40, 10, DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
('Tomate Rojo kg', 9, 1.00, 1.80, 70, 20, DATE_ADD(CURDATE(), INTERVAL 4 DAY)),
('Lechuga Fresca', 9, 0.80, 1.50, 45, 10, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Cebolla Blanca kg', 9, 0.70, 1.30, 85, 25, DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
('Ajo Blanco kg', 9, 1.80, 3.00, 35, 8, DATE_ADD(CURDATE(), INTERVAL 30 DAY)),
('Zanahoria kg', 9, 0.60, 1.20, 70, 20, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Aguacate kg', 9, 2.00, 3.50, 30, 8, DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
('Brócoli Fresco', 9, 1.50, 2.50, 25, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Pepino kg', 9, 0.80, 1.50, 50, 12, DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
('Piña Fresca', 9, 1.50, 2.80, 35, 8, DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
('Limón Fresco kg', 9, 1.00, 1.80, 60, 15, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Pimiento Rojo kg', 9, 1.80, 3.00, 25, 5, DATE_ADD(CURDATE(), INTERVAL 5 DAY));

-- Carne y Embutidos (11 productos)
INSERT INTO productos (nombre, categoria_id, precio_compra, precio_venta, stock, stock_minimo, fecha_vencimiento) VALUES
('Jamón Prosciutto 100g', 10, 2.50, 4.50, 30, 5, DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
('Salchichas x5 300g', 10, 1.50, 2.50, 45, 10, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Pechuga de Pollo kg', 10, 3.00, 5.50, 40, 10, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Carne Molida kg', 10, 4.00, 7.00, 35, 8, DATE_ADD(CURDATE(), INTERVAL 2 DAY)),
('Bistec de Res kg', 10, 5.50, 9.50, 25, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Mortadela 500g', 10, 2.00, 3.50, 40, 8, DATE_ADD(CURDATE(), INTERVAL 20 DAY)),
('Chorizo Español 400g', 10, 3.00, 5.00, 25, 5, DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
('Huevos x12 Unidades', 10, 2.50, 4.00, 60, 20, DATE_ADD(CURDATE(), INTERVAL 20 DAY)),
('Costilla de Cerdo kg', 10, 4.50, 7.50, 20, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
('Tocino 250g', 10, 2.50, 4.00, 30, 8, DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
('Filete de Tilapia kg', 10, 5.00, 8.50, 22, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY));

-- =====================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- =====================================================
CREATE INDEX idx_productos_fecha_vencimiento ON productos(fecha_vencimiento);
CREATE INDEX idx_detalle_ventas_fecha ON detalle_ventas(venta_id);
CREATE INDEX idx_ventas_metodo_pago ON ventas(metodo_pago);

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================
SELECT COUNT(*) as total_categorias FROM categorias;
SELECT COUNT(*) as total_productos FROM productos;
SELECT SUM(stock) as stock_total FROM productos;

-- =====================================================
-- SCRIPT DE VENTAS SIMULADAS - MES COMPLETO
-- =====================================================

USE mini_super_botargas;

-- =====================================================
-- CONFIGURACIÓN INICIAL
-- =====================================================

-- Variables de configuración
SET @mes_simulado = '2024-01-01';  -- Cambiar por el mes deseado
SET @dias_mes = 31;                -- Días del mes a simular
SET @ventas_min_dia = 15;          -- Mínimo de ventas por día
SET @ventas_max_dia = 45;          -- Máximo de ventas por día
SET @productos_min_venta = 1;      -- Mínimo de productos por venta
SET @productos_max_venta = 8;      -- Máximo de productos por venta

-- =====================================================
-- FUNCIONES AUXILIARES
-- =====================================================

-- Función para generar número aleatorio en rango
DELIMITER //
CREATE FUNCTION random_range(min_val INT, max_val INT) 
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN FLOOR(RAND() * (max_val - min_val + 1)) + min_val;
END//

-- Función para generar fecha aleatoria en un día específico
CREATE FUNCTION random_fecha_en_dia(dia DATE) 
RETURNS DATETIME
DETERMINISTIC
BEGIN
    DECLARE hora_aleatoria TIME;
    SET hora_aleatoria = SEC_TO_TIME(FLOOR(RAND() * 86400));
    RETURN TIMESTAMP(dia, hora_aleatoria);
END//

DELIMITER ;

-- =====================================================
-- PROCEDIMIENTO PARA GENERAR VENTAS DEL MES
-- =====================================================

DELIMITER //

CREATE PROCEDURE generar_ventas_mes()
BEGIN
    DECLARE dia_actual INT DEFAULT 1;
    DECLARE fecha_actual DATE;
    DECLARE total_ventas_dia INT;
    DECLARE contador_venta INT;
    DECLARE hora_venta TIME;
    DECLARE id_venta INT;
    DECLARE total_venta DECIMAL(10,2);
    
    DECLARE exit_handler BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET exit_handler = TRUE;
    
    -- Desactivar autocommit para mejor performance
    SET autocommit = 0;
    
    -- Limpiar ventas existentes (opcional, comentar si no se desea)
    -- DELETE FROM detalle_ventas;
    -- DELETE FROM ventas;
    
    WHILE dia_actual <= @dias_mes DO
        SET fecha_actual = DATE_ADD(@mes_simulado, INTERVAL (dia_actual - 1) DAY);
        SET total_ventas_dia = random_range(@ventas_min_dia, @ventas_max_dia);
        SET contador_venta = 1;
        
        -- Generar ventas para el día actual
        WHILE contador_venta <= total_ventas_dia DO
            -- Generar hora aleatoria distribuida según patrones reales
            SET hora_venta = generar_hora_realista();
            
            -- Insertar venta principal
            INSERT INTO ventas (fecha, hora, total, metodo_pago, estado)
            VALUES (fecha_actual, hora_venta, 0, generar_metodo_pago(), 'Completada');
            
            SET id_venta = LAST_INSERT_ID();
            SET total_venta = 0;
            
            -- Generar detalles de la venta
            CALL generar_detalle_venta(id_venta, total_venta);
            
            -- Actualizar total de la venta
            UPDATE ventas SET total = total_venta WHERE id = id_venta;
            
            SET contador_venta = contador_venta + 1;
        END WHILE;
        
        -- Commit cada día para no perder todo en caso de error
        COMMIT;
        SET dia_actual = dia_actual + 1;
    END WHILE;
    
    -- Reactivar autocommit
    SET autocommit = 1;
    
    SELECT CONCAT('Ventas generadas: ', (SELECT COUNT(*) FROM ventas)) as resultado;
END//

-- Función para generar hora realista según patrones de venta
CREATE FUNCTION generar_hora_realista() 
RETURNS TIME
DETERMINISTIC
BEGIN
    DECLARE hora TIME;
    DECLARE rnd FLOAT;
    SET rnd = RAND();
    
    -- Distribución de horas según patrones típicos de supermercado:
    -- 15% madrugada (00:00-06:00)
    -- 20% mañana (06:00-12:00) 
    -- 35% tarde (12:00-18:00)
    -- 30% noche (18:00-24:00)
    
    IF rnd < 0.15 THEN
        -- Madrugada: menos ventas
        SET hora = SEC_TO_TIME(FLOOR(RAND() * 21600)); -- 0-6 horas
    ELSEIF rnd < 0.35 THEN
        -- Mañana: ventas moderadas
        SET hora = SEC_TO_TIME(21600 + FLOOR(RAND() * 21600)); -- 6-12 horas
    ELSEIF rnd < 0.70 THEN
        -- Tarde: más ventas
        SET hora = SEC_TO_TIME(43200 + FLOOR(RAND() * 21600)); -- 12-18 horas
    ELSE
        -- Noche: ventas moderadas-altas
        SET hora = SEC_TO_TIME(64800 + FLOOR(RAND() * 21600)); -- 18-24 horas
    END IF;
    
    RETURN hora;
END//

-- Función para generar método de pago realista
CREATE FUNCTION generar_metodo_pago() 
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE metodo VARCHAR(50);
    DECLARE rnd FLOAT;
    SET rnd = RAND();
    
    -- Distribución típica de métodos de pago
    IF rnd < 0.55 THEN
        SET metodo = 'Efectivo';
    ELSEIF rnd < 0.85 THEN
        SET metodo = 'Tarjeta Débito';
    ELSEIF rnd < 0.95 THEN
        SET metodo = 'Tarjeta Crédito';
    ELSE
        SET metodo = 'Transferencia';
    END IF;
    
    RETURN metodo;
END//

-- Procedimiento para generar detalles de venta
CREATE PROCEDURE generar_detalle_venta(IN venta_id INT, INOUT total_venta DECIMAL(10,2))
BEGIN
    DECLARE num_productos INT;
    DECLARE contador_producto INT DEFAULT 1;
    DECLARE producto_seleccionado INT;
    DECLARE cantidad_producto INT;
    DECLARE precio_unitario DECIMAL(10,2);
    DECLARE subtotal_producto DECIMAL(10,2);
    DECLARE stock_actual INT;
    
    -- Número de productos en esta venta
    SET num_productos = random_range(@productos_min_venta, @productos_max_venta);
    
    WHILE contador_producto <= num_productos DO
        -- Seleccionar producto aleatorio que tenga stock
        SELECT id, precio_venta, stock INTO producto_seleccionado, precio_unitario, stock_actual
        FROM productos 
        WHERE stock > 0 AND activo = TRUE
        ORDER BY RAND() 
        LIMIT 1;
        
        -- Si encontramos producto con stock
        IF producto_seleccionado IS NOT NULL THEN
            -- Cantidad aleatoria, máximo 5 unidades o el stock disponible
            SET cantidad_producto = LEAST(random_range(1, 5), stock_actual);
            SET subtotal_producto = precio_unitario * cantidad_producto;
            SET total_venta = total_venta + subtotal_producto;
            
            -- Insertar detalle
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (venta_id, producto_seleccionado, cantidad_producto, precio_unitario, subtotal_producto);
            
            -- Actualizar stock del producto
            UPDATE productos 
            SET stock = stock - cantidad_producto 
            WHERE id = producto_seleccionado;
        END IF;
        
        SET contador_producto = contador_producto + 1;
    END WHILE;
END//

DELIMITER ;

-- =====================================================
-- EJECUTAR GENERACIÓN DE VENTAS
-- =====================================================

-- Ejecutar el procedimiento principal
CALL generar_ventas_mes();

-- =====================================================
-- CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Resumen de ventas generadas
SELECT 
    COUNT(*) as total_ventas,
    SUM(total) as ingreso_total,
    AVG(total) as ticket_promedio,
    MIN(fecha) as primera_fecha,
    MAX(fecha) as ultima_fecha
FROM ventas;

-- Ventas por día
SELECT 
    fecha,
    COUNT(*) as ventas_dia,
    SUM(total) as ingreso_dia,
    AVG(total) as ticket_promedio_dia
FROM ventas 
GROUP BY fecha 
ORDER BY fecha;

-- Distribución por método de pago
SELECT 
    metodo_pago,
    COUNT(*) as cantidad_ventas,
    SUM(total) as monto_total,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ventas)), 2) as porcentaje
FROM ventas 
GROUP BY metodo_pago 
ORDER BY cantidad_ventas DESC;

-- Distribución por hora del día
SELECT 
    CASE 
        WHEN HOUR(hora) BETWEEN 0 AND 5 THEN 'Madrugada (00-06)'
        WHEN HOUR(hora) BETWEEN 6 AND 11 THEN 'Mañana (06-12)'
        WHEN HOUR(hora) BETWEEN 12 AND 17 THEN 'Tarde (12-18)'
        ELSE 'Noche (18-24)'
    END as periodo,
    COUNT(*) as ventas,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ventas)), 2) as porcentaje
FROM ventas 
GROUP BY periodo 
ORDER BY FIELD(periodo, 'Madrugada (00-06)', 'Mañana (06-12)', 'Tarde (12-18)', 'Noche (18-24)');

-- Top 10 productos más vendidos
SELECT 
    p.nombre,
    p.categoria_id,
    c.nombre as categoria,
    SUM(dv.cantidad) as total_vendido,
    SUM(dv.subtotal) as ingreso_generado
FROM detalle_ventas dv
JOIN productos p ON dv.producto_id = p.id
JOIN categorias c ON p.categoria_id = c.id
GROUP BY p.id, p.nombre, p.categoria_id, c.nombre
ORDER BY total_vendido DESC
LIMIT 10;

-- Productos con stock bajo después de las ventas
SELECT 
    nombre,
    stock,
    stock_minimo,
    fecha_vencimiento
FROM productos 
WHERE stock <= stock_minimo 
ORDER BY stock ASC;

-- =====================================================
-- LIMPIAR FUNCIONES Y PROCEDIMIENTOS TEMPORALES
-- =====================================================

DROP FUNCTION IF EXISTS random_range;
DROP FUNCTION IF EXISTS random_fecha_en_dia;
DROP FUNCTION IF EXISTS generar_hora_realista;
DROP FUNCTION IF EXISTS generar_metodo_pago;
DROP PROCEDURE IF EXISTS generar_detalle_venta;
DROP PROCEDURE IF EXISTS generar_ventas_mes;