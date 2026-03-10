from app.database.connection import get_connection


# 1 Ver habitaciones.
def get_rooms():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM habitaciones;")
            return cur.fetchall()

# 2 ver disponibilidad.
def get_available_rooms():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM habitaciones WHERE disponibilidad = TRUE;")
            return cur.fetchall()
        
# 3 Crear Reservacion.
def create_reservation(id_number, name, room_id, checkin, checkout):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "SELECT * FROM create_reservation(%s, %s, %s, %s, %s);",
                    (id_number, name, room_id, checkin, checkout)
                )

                resultado = cur.fetchone()
                reserva_id = resultado['create_reservation']  # 👈 fix
                conn.commit()

                return {"id": reserva_id}

            except Exception as e:
                conn.rollback()
                print(f"Error tipo: {type(e).__name__}")
                print(f"Error detalle: {e}")
                return None
# def create_reservation(id_number, name, room_id, checkin, checkout):
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             try:
#                 # 1. Buscar huesped, si existe o sino crearlo.
#                 # usamo el id_number
#                 cur.execute(
#                     """
#                     INSERT INTO huespedes (id_number, nombre)
#                     VALUES (%s, %s)
#                     ON CONFLICT (id_number) DO UPDATE SET nombre = EXCLUDED.nombre
#                     RETURNING id;
#                     """,
#                     (id_number, name)
#                 )
#                 huesped_id = cur.fetchone()["id"]

#                 # 2 Insertar la Reservar usando huesped_id obtenido.
#                 cur.execute(
#                     """
#                     INSERT INTO reservas
#                     (habitacion_id, fecha_inicio, fecha_fin, status, huesped_id)
#                     VALUES (%s, %s, %s, 'pendiente', %s)
#                     RETURNING id;
#                     """,
#                     (room_id, checkin, checkout, huesped_id)
#                 )

#                 reserva =  cur.fetchone()
#                 conn.commit() # confirmación de ambos cambios.
#                 return reserva

#             except Exception as e:
#                 conn.rollback() # si algo falla, deshacer todo.
#                 print(f"Error en la reservar {e}")
#                 return None

# Consultar Reservas por id_number
def get_reservations_by_id(id_number):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_reservations_by_id_number(%s);",
                (id_number, )
            )
            consulta = cur.fetchall()
            return consulta
        

# Function to do the Check-in
def do_checkin(reserva_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT do_checkin(%s);", (reserva_id,))
                conn.commit()
                return {"success": True, "message": f"Check-in realizado para reserva {reserva_id}"}
            except Exception as e:
                conn.rollback()
                print(f"Error en check-in: {e}")
                return {"success": False, "message": str(e)}


# python function to do the Check-out
def do_checkout(reserva_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT do_checkout(%s);", (reserva_id,))
                conn.commit()
                return {"success": True, "message": f"Check-out realizado para reserva {reserva_id}"}
            except Exception as e:
                conn.rollback()
                print(f"Error en check-out: {e}")
                return {"success": False, "message": str(e)}
            

# create main
if __name__== '__main__':
        
    # Intentar crear la reserva
    reservation = create_reservation('87600001', 'George caceres', 1, '2026-03-23', '2026-03-26')
    print(reservation)
        