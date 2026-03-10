-- 2. Tabla de Huéspedes
CREATE TABLE huespedes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

-- insertar una nueva reserva.
 INSERT INTO reservas
                (habitacion_id,fecha_inicio,fecha_fin,status,huesped_id)
                VALUES (1,'2026-04-01','2026-03-02','cancelado',3)
                RETURNING id;


-- buscar usuario si ya existe y si no crearlo.
                    INSERT INTO huespedes (nombre, email)
                    VALUES ('', %s)
                    ON CONFLICT (email) DO UPDATE SET nombre = EXCLUDED.nombre
                    RETURNING id;

-- agregamos id_number / passport number
ALTER TABLE huespedes ADD COLUMN id_number VARCHAR(12) UNIQUE;
UPDATE huespedes SET id_number = '12345678' WHERE id = 1; -- Roberto Gomez
UPDATE huespedes SET id_number = '87654321' WHERE id = 2; -- Maria Lopez
UPDATE huespedes SET id_number = '11223344' WHERE id = 3; -- Juan Perez
UPDATE huespedes SET id_number = '44332211' WHERE id = 4; -- Carlos Ruiz
UPDATE huespedes SET id_number = '99887766' WHERE id = 5; -- Ana Garcia


CREATE OR REPLACE FUNCTION get_reservations_by_id_number(p_id_number VARCHAR)
RETURNS TABLE (
    reserva_id      INT,
    habitacion_id   INT,
    numero_hab      INT,
    tipo_hab        VARCHAR,
    precio_noche    NUMERIC,
    fecha_inicio    DATE,
    fecha_fin       DATE,
    status          estado_reserva,
    huesped_nombre  VARCHAR,
    huesped_email   VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Verificar si el huesped existe
    IF NOT EXISTS (SELECT 1 FROM huespedes WHERE id_number = p_id_number) THEN
        RAISE EXCEPTION 'Huesped con id_number % no encontrado', p_id_number;
    END IF;

    -- 2. Retornar reservas con info completa
    RETURN QUERY
    SELECT 
        r.id,
        r.habitacion_id,
        h.numero,
        h.tipo::VARCHAR,
        h.precio_noche,
        r.fecha_inicio,
        r.fecha_fin,
        r.status,
        g.nombre,
        g.email
    FROM reservas r
    JOIN huespedes g ON r.huesped_id = g.id
    JOIN habitaciones h ON r.habitacion_id = h.id
    WHERE g.id_number = p_id_number;
END;
$$;


--- eliminar privilegios previos para user hotel_user y 
--- otorgar solo los necesarios para el agente.
REVOKE ALL PRIVILEGES ON TABLE reservas FROM hotel_user;
REVOKE ALL PRIVILEGES ON TABLE habitaciones FROM hotel_user;
REVOKE ALL PRIVILEGES ON TABLE huespedes FROM hotel_user;

--- dar acceso a lectura y solo insertar a algunas tablas,
--- sin delete, update or algo que provoque mas uso sql injection.
GRANT SELECT ON habitaciones TO hotel_user;
GRANT SELECT, INSERT ON reservas TO hotel_user;
GRANT SELECT, INSERT ON huespedes TO hotel_user;

--- permiter y dar permisos para generar el sgt id automatico y correcto al insertar.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hotel_user;