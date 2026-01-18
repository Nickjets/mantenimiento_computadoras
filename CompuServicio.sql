------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--CREAR LA BASE DE DATOS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Database: CompuMercado
-- DROP DATABASE IF EXISTS "CompuMercado";
CREATE DATABASE "CompuMercado"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Ecuador.1252'
    LC_CTYPE = 'Spanish_Ecuador.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--CREACION DE TABLAS
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Tabla CLIENTE
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT
);

-- Tabla EQUIPO
CREATE TABLE equipo (
    id_equipo SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    tipo_equipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(50) UNIQUE,
    observaciones_fisicas TEXT,
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);

-- Tabla TECNICO
CREATE TABLE tecnico (
    id_tecnico SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(20)
);

-- Tabla CATALOGO_SERVICIO
CREATE TABLE catalogo_servicio (
    id_servicio SERIAL PRIMARY KEY,
    nombre_servicio VARCHAR(100) NOT NULL,
    precio_base DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    descripcion TEXT
);

-- Tabla REPUESTO
CREATE TABLE repuesto (
    id_repuesto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(50),
    stock_actual INT NOT NULL DEFAULT 0,
    precio_unitario DECIMAL(10, 2) NOT NULL
);

-- Tabla ORDEN_SERVICIO
CREATE TABLE orden_servicio (
    id_orden SERIAL PRIMARY KEY,
    id_equipo INT NOT NULL,
    id_cliente INT NOT NULL,
    id_tecnico INT,
    fecha_recepcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_estimada_entrega DATE,
    estado VARCHAR(20) NOT NULL,
    problema_reportado TEXT NOT NULL,
    diagnostico_tecnico TEXT,
    total_estimado DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
	FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico)
);

-- Tabla DETALLE_ORDEN_SERVICIO
CREATE TABLE detalle_orden_servicio (
    id_detalle_serv SERIAL PRIMARY KEY,
    id_orden INT NOT NULL,
    id_servicio INT NOT NULL,
    precio_aplicado DECIMAL(10, 2) NOT NULL,
    observacion TEXT,
    FOREIGN KEY (id_orden) REFERENCES orden_servicio(id_orden) ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES catalogo_servicio(id_servicio)
);

-- Tabla DETALLE_ORDEN_REPUESTO
CREATE TABLE detalle_orden_repuesto (
    id_detalle_repuesto SERIAL PRIMARY KEY,
    id_orden INT NOT NULL,
    id_repuesto INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precoin_venta DECIMAL(10, 2) NOT NULL,
	FOREIGN KEY (id_orden) REFERENCES orden_servicio(id_orden) ON DELETE CASCADE,
    FOREIGN KEY (id_repuesto) REFERENCES repuesto(id_repuesto)
);


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--DATOS DE EJEMPLO
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

INSERT INTO cliente (cedula, nombres, apellidos, telefono, email, direccion) VALUES
('1234567890', 'Juan', 'Pérez', '0991234567', 'juan@email.com', 'Calle Principal 123'),
('0987654321', 'María', 'González', '0987654321', 'maria@email.com', 'Avenida Central 456');

INSERT INTO equipo (id_cliente, tipo_equipo, marca, modelo, numero_serie, observaciones_fisicas) VALUES
(1, 'Laptop', 'HP', 'Pavilion 15', 'HP123456', 'Rayones en la tapa'),
(2, 'PC Escritorio', 'Dell', 'Optiplex 3020', 'DL789012', 'Sin observaciones');

INSERT INTO tecnico (cedula, nombres, apellidos, especialidad, telefono) VALUES
('1112223334', 'Carlos', 'Martínez', 'Electrónica', '0971112223'),
('4445556667', 'Ana', 'Rodríguez', 'Software', '0984445556');

INSERT INTO catalogo_servicio (nombre_servicio, precio_base, descripcion) VALUES
('Diagnóstico general', 25.00, 'Revisión completa del equipo'),
('Limpieza interna', 40.00, 'Limpieza de componentes internos'),
('Instalación de SO', 60.00, 'Instalación de sistema operativo');

INSERT INTO repuesto (nombre, marca, stock_actual, precio_unitario) VALUES
('Memoria RAM 8GB', 'Kingston', 10, 45.00),
('Disco SSD 500GB', 'Samsung', 8, 85.00),
('Batería Laptop', 'Generic', 5, 65.00);

INSERT INTO orden_servicio(id_equipo,id_cliente,id_tecnico,fecha_recepcion,fecha_estimada_entrega,estado,problema_reportado,diagnostico_tecnico,total_estimado) VALUES
(1, 1, 1, '2024-01-15 09:30:00', '2024-01-20', 'ENTREGADO', 
 'No enciende, hace sonido de beep', 
 'Falló la memoria RAM. Se reemplazó y se hizo limpieza interna', 
 110.00),
-- Orden 2: PC Dell lento
(2, 2, 2, '2024-01-18 14:15:00', '2024-01-22', 'ENTREGADO',
 'Muy lento, tarda en abrir programas',
 'Disco duro dañado. Se reemplazó por SSD y se instaló SO nuevo',
 185.00)

INSERT INTO detalle_orden_servicio (id_orden, id_servicio, precio_aplicado, observacion) VALUES
-- Orden 1
(1, 1, 25.00, 'Diagnóstico incluido en reparación'),
(1, 2, 40.00, 'Limpieza profunda por polvo acumulado'),
-- Orden 2
(2, 1, 25.00, 'Diagnóstico de velocidad'),
(2, 3, 60.00, 'Instalación Windows 11 Pro')

INSERT INTO detalle_orden_repuesto (id_orden, id_repuesto, cantidad, precoin_venta) VALUES
-- Orden 1: Se usó memoria RAM
(1, 1, 1, 50.00),  -- RAM Kingston 8GB
-- Orden 2: Se usó SSD
(2, 2, 1, 100.00) -- SSD Samsung 500GB

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VISTAS PARA REPORTES
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- 1. Vista para órdenes de servicio con información completa
CREATE OR REPLACE VIEW vista_ordenes_completas AS
SELECT 
    os.id_orden,
    os.fecha_recepcion,
    os.fecha_estimada_entrega,
    os.estado,
    os.problema_reportado,
    os.diagnostico_tecnico,
    os.total_estimado,
    -- Información del cliente
    c.id_cliente,
    c.cedula as cedula_cliente,
    c.nombres || ' ' || c.apellidos as cliente_completo,
    c.telefono as telefono_cliente,
    c.email as email_cliente,
    -- Información del equipo
    e.id_equipo,
    e.tipo_equipo,
    e.marca as marca_equipo,
    e.modelo as modelo_equipo,
    e.numero_serie,
    -- Información del técnico
    t.id_tecnico,
    t.nombres || ' ' || t.apellidos as tecnico_completo,
    t.especialidad,
    t.telefono as telefono_tecnico
FROM orden_servicio os
JOIN cliente c ON os.id_cliente = c.id_cliente
JOIN equipo e ON os.id_equipo = e.id_equipo
LEFT JOIN tecnico t ON os.id_tecnico = t.id_tecnico;


-- 2. Vista para órdenes pendientes/activas
CREATE OR REPLACE VIEW vista_ordenes_activas AS
SELECT 
    id_orden,
    fecha_recepcion,
    fecha_estimada_entrega,
    estado,
    cliente_completo,
    telefono_cliente,
    tipo_equipo || ' ' || marca_equipo || ' ' || modelo_equipo as equipo,
    tecnico_completo,
    total_estimado,
    -- Días transcurridos y días restantes
    CURRENT_DATE - DATE(fecha_recepcion) as dias_transcurridos,
    fecha_estimada_entrega - CURRENT_DATE as dias_restantes
FROM vista_ordenes_completas
WHERE estado IN ('RECIBIDO', 'EN DIAGNOSTICO', 'EN REPARACION', 'ESPERANDO REPUESTOS')
ORDER BY fecha_recepcion DESC;


-- 3. Vista para inventario bajo de stock
CREATE OR REPLACE VIEW vista_inventario_bajo AS
SELECT 
    r.id_repuesto,
    r.nombre,
    r.marca,
    r.stock_actual,
    r.precio_unitario,
    CASE 
        WHEN r.stock_actual = 0 THEN 'AGOTADO'
        WHEN r.stock_actual <= 3 THEN 'CRÍTICO'
        WHEN r.stock_actual <= 5 THEN 'BAJO'
        ELSE 'NORMAL'
    END as nivel_stock,
    -- Cantidad usada en últimos 30 días
    COALESCE(SUM(dr.cantidad), 0) as usado_ultimos_30dias
FROM repuesto r
LEFT JOIN detalle_orden_repuesto dr ON r.id_repuesto = dr.id_repuesto
LEFT JOIN orden_servicio os ON dr.id_orden = os.id_orden 
    AND os.fecha_recepcion >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY r.id_repuesto, r.nombre, r.marca, r.stock_actual, r.precio_unitario
HAVING r.stock_actual <= 5
ORDER BY r.stock_actual ASC;


-- 4. Vista para reporte de técnicos (productividad)
CREATE OR REPLACE VIEW vista_rendimiento_tecnicos AS
SELECT 
    t.id_tecnico,
    t.cedula,
    t.nombres || ' ' || t.apellidos as tecnico,
    t.especialidad,
    -- Estadísticas
    COUNT(DISTINCT os.id_orden) as total_ordenes_atendidas,
    SUM(os.total_estimado) as total_facturado,
    AVG(os.total_estimado) as promedio_por_orden,
    -- Tiempo promedio de reparación (días)
    AVG(DATE(os.fecha_estimada_entrega) - DATE(os.fecha_recepcion)) as tiempo_promedio_reparacion,
    -- Ordenes por estado
    COUNT(CASE WHEN os.estado = 'ENTREGADO' THEN 1 END) as ordenes_entregadas,
    COUNT(CASE WHEN os.estado = 'EN REPARACION' THEN 1 END) as ordenes_en_proceso,
    COUNT(CASE WHEN os.estado = 'CANCELADO' THEN 1 END) as ordenes_canceladas
FROM tecnico t
LEFT JOIN orden_servicio os ON t.id_tecnico = os.id_tecnico
    AND os.fecha_recepcion >= CURRENT_DATE - INTERVAL '90 days' -- Últimos 90 días
GROUP BY t.id_tecnico, t.cedula, t.nombres, t.apellidos, t.especialidad
ORDER BY total_facturado DESC;


-- 5. Vista para servicios más solicitados
CREATE OR REPLACE VIEW vista_servicios_populares AS
SELECT 
    cs.id_servicio,
    cs.nombre_servicio,
    cs.precio_base,
    COUNT(ds.id_detalle_serv) as veces_solicitado,
    SUM(ds.precio_aplicado) as ingreso_total,
    AVG(ds.precio_aplicado) as precio_promedio_aplicado,
    -- Mes actual vs mes anterior
    COUNT(CASE WHEN DATE_TRUNC('month', os.fecha_recepcion) = DATE_TRUNC('month', CURRENT_DATE) 
        THEN 1 END) as solicitudes_mes_actual,
    COUNT(CASE WHEN DATE_TRUNC('month', os.fecha_recepcion) = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') 
        THEN 1 END) as solicitudes_mes_anterior
FROM catalogo_servicio cs
LEFT JOIN detalle_orden_servicio ds ON cs.id_servicio = ds.id_servicio
LEFT JOIN orden_servicio os ON ds.id_orden = os.id_orden
    AND os.fecha_recepcion >= CURRENT_DATE - INTERVAL '180 days' -- Últimos 6 meses
GROUP BY cs.id_servicio, cs.nombre_servicio, cs.precio_base
ORDER BY veces_solicitado DESC;


-- 6. Vista para clientes frecuentes
CREATE OR REPLACE VIEW vista_clientes_frecuentes AS
SELECT 
    c.id_cliente,
    c.cedula,
    c.nombres || ' ' || c.apellidos as cliente,
    c.telefono,
    c.email,
    -- Estadísticas
    COUNT(DISTINCT os.id_orden) as total_ordenes,
    COUNT(DISTINCT e.id_equipo) as equipos_registrados,
    SUM(os.total_estimado) as total_gastado,
    MAX(os.fecha_recepcion) as ultima_visita,
    -- Ordenes por estado
    COUNT(CASE WHEN os.estado = 'ENTREGADO' THEN 1 END) as ordenes_completadas,
    COUNT(CASE WHEN os.estado = 'EN REPARACION' THEN 1 END) as ordenes_pendientes,
    -- Promedio de gasto
    AVG(os.total_estimado) as gasto_promedio_por_orden
FROM cliente c
LEFT JOIN equipo e ON c.id_cliente = e.id_cliente
LEFT JOIN orden_servicio os ON c.id_cliente = os.id_cliente
GROUP BY c.id_cliente, c.cedula, c.nombres, c.apellidos, c.telefono, c.email
ORDER BY total_gastado DESC NULLS LAST;


-- 7. Vista para reporte financiero mensual
CREATE OR REPLACE VIEW vista_financiero_mensual AS
SELECT 
    DATE_TRUNC('month', os.fecha_recepcion) as mes,
    TO_CHAR(DATE_TRUNC('month', os.fecha_recepcion), 'Month YYYY') as mes_nombre,
    -- Totales
    COUNT(DISTINCT os.id_orden) as total_ordenes,
    SUM(os.total_estimado) as ingresos_totales,
    -- Ingresos por categoría
    COALESCE(SUM(ds.precio_aplicado), 0) as ingresos_servicios,
    COALESCE(SUM(dr.cantidad * dr.precoin_venta), 0) as ingresos_repuestos,
    -- Promedios
    AVG(os.total_estimado) as promedio_por_orden,
    -- Información adicional usando funciones de ventana
    MAX(os.fecha_recepcion) as ultima_fecha_recepcion
FROM orden_servicio os
LEFT JOIN detalle_orden_servicio ds ON os.id_orden = ds.id_orden
LEFT JOIN detalle_orden_repuesto dr ON os.id_orden = dr.id_orden
WHERE os.estado = 'ENTREGADO'
GROUP BY DATE_TRUNC('month', os.fecha_recepcion)
ORDER BY mes DESC;


--8. Vista de equipos 'Abandonados'
CREATE OR REPLACE VIEW vista_equipos_abandonados AS
SELECT 
    os.id_orden,
    c.nombres || ' ' || c.apellidos as cliente,
    c.telefono as telefono_cliente,
    c.email as email_cliente,
    e.tipo_equipo,
    e.marca,
    e.modelo,
    e.numero_serie,
    os.estado,
    os.fecha_recepcion,
    os.fecha_estimada_entrega,
    CURRENT_DATE - DATE(os.fecha_recepcion) as dias_en_taller,
    CASE 
        WHEN CURRENT_DATE - DATE(os.fecha_recepcion) > 45 THEN 'CRÍTICO'
        WHEN CURRENT_DATE - DATE(os.fecha_recepcion) > 30 THEN 'ALTO'
        ELSE 'MODERADO'
    END as nivel_alerta,
    t.nombres || ' ' || t.apellidos as tecnico_asignado,
    t.telefono as telefono_tecnico,
    os.problema_reportado
FROM orden_servicio os
JOIN cliente c ON os.id_cliente = c.id_cliente
JOIN equipo e ON os.id_equipo = e.id_equipo
LEFT JOIN tecnico t ON os.id_tecnico = t.id_tecnico
WHERE os.estado NOT IN ('ENTREGADO', 'CANCELADO')  -- Excluir órdenes finalizadas
AND CURRENT_DATE - DATE(os.fecha_recepcion) > 30  -- Más de 30 días
ORDER BY dias_en_taller DESC, os.fecha_recepcion;


-- 9.Vista de Ingresos por Técnico del Mes Actual
CREATE OR REPLACE VIEW vista_ingresos_tecnicos_mes AS
SELECT 
    t.id_tecnico,
    t.cedula,
    t.nombres || ' ' || t.apellidos as tecnico,
    COUNT(DISTINCT os.id_orden) as ordenes_atendidas_mes
FROM tecnico t
LEFT JOIN orden_servicio os ON t.id_tecnico = os.id_tecnico
    AND EXTRACT(MONTH FROM os.fecha_recepcion) = EXTRACT(MONTH FROM CURRENT_DATE)
    AND EXTRACT(YEAR FROM os.fecha_recepcion) = EXTRACT(YEAR FROM CURRENT_DATE)
    AND os.estado = 'ENTREGADO'
GROUP BY t.id_tecnico, t.cedula, t.nombres, t.apellidos
ORDER BY ordenes_atendidas_mes DESC;


-- 10. Vista de Servicios Solicitados en el Mes Actual
CREATE OR REPLACE VIEW vista_servicios_mes AS
WITH mes_actual AS (
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) as inicio_mes,
        (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month' - INTERVAL '1 day') as fin_mes
)
SELECT 
    cs.id_servicio,
    cs.nombre_servicio,
    COUNT(DISTINCT dos.id_detalle_serv) as veces_solicitado_mes
FROM catalogo_servicio cs
CROSS JOIN mes_actual ma
LEFT JOIN detalle_orden_servicio dos ON cs.id_servicio = dos.id_servicio
LEFT JOIN orden_servicio os ON dos.id_orden = os.id_orden
    AND os.fecha_recepcion >= ma.inicio_mes
    AND os.fecha_recepcion <= ma.fin_mes
    AND os.estado = 'ENTREGADO'
GROUP BY cs.id_servicio, cs.nombre_servicio
ORDER BY veces_solicitado_mes DESC;


