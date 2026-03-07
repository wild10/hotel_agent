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


-- CHECK IN: cambia status a 'confirmada' y marca habitacion como no disponible
CREATE OR REPLACE FUNCTION do_checkin(p_reserva_id INT)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar que la reserva existe y está pendiente
    IF NOT EXISTS (SELECT 1 FROM reservas WHERE id = p_reserva_id AND status = 'pendiente') THEN
        RAISE EXCEPTION 'Reserva % no encontrada o no está en estado pendiente', p_reserva_id;
    END IF;

    -- Actualizar status de la reserva
    UPDATE reservas SET status = 'confirmada' WHERE id = p_reserva_id;

    -- Marcar habitacion como no disponible
    UPDATE habitaciones SET disponibilidad = false
    WHERE id = (SELECT habitacion_id FROM reservas WHERE id = p_reserva_id);
END;
$$;


-- CHECKOUT: cambia status a 'finalizada' y libera la habitacion
CREATE OR REPLACE FUNCTION do_checkout(p_reserva_id INT)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar que la reserva existe y está confirmada
    IF NOT EXISTS (SELECT 1 FROM reservas WHERE id = p_reserva_id AND status = 'confirmada') THEN
        RAISE EXCEPTION 'Reserva % no encontrada o no está en estado confirmada', p_reserva_id;
    END IF;

    -- Actualizar status de la reserva
    UPDATE reservas SET status = 'finalizada' WHERE id = p_reserva_id;

    -- Liberar la habitacion
    UPDATE habitaciones SET disponibilidad = true
    WHERE id = (SELECT habitacion_id FROM reservas WHERE id = p_reserva_id);
END;
$$;
