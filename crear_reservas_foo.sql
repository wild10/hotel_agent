CREATE OR REPLACE FUNCTION create_reservation(
    p_id_number TEXT,
    p_name TEXT,
    p_room_id INT,
    p_checkin DATE,
    p_checkout DATE
)
RETURNS INT
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_huesped_id INT;
    v_reserva_id INT;
BEGIN

    -- 1. Crear o actualizar huésped
    INSERT INTO huespedes (id_number, nombre)
    VALUES (p_id_number, p_name)
    ON CONFLICT (id_number)
    DO UPDATE SET nombre = EXCLUDED.nombre
    RETURNING id INTO v_huesped_id;

    -- 2. Crear reserva
    INSERT INTO reservas (
        habitacion_id,
        fecha_inicio,
        fecha_fin,
        status,
        huesped_id
    )
    VALUES (
        p_room_id,
        p_checkin,
        p_checkout,
        'pendiente',
        v_huesped_id
    )
    RETURNING id INTO v_reserva_id;

    RETURN v_reserva_id;

END;
$$;