# Exponemos las queries como tools para el agente.

# cargamos las queries.
from app.database.queries import (
    create_reservation,
    do_checkin,
    do_checkout,
    get_available_rooms,
    get_reservations_by_id,
    get_rooms,
)
from langchain_core.tools import tool

# cargamos RAG
from app.rag.pipeline import generate_answer


@tool
def tool_get_hotel_info_rag(pregunta: str) -> str:

    """
    Retorna informacion sobre el hotel y servicios , politicas.
    Úsalas cuando el usuario quiera saber sobre preguntas frecuentes,
    politicas del hotel, servicioes adicionales, información del hotel.
    """
    return generate_answer(pregunta)

@tool
def tool_get_rooms() -> str:
    """
    Retorna todas la habitaciones del hotel con detalles.
    úsalas cuando el usuario quiera ver todas las habitaciones disponibles o
    informacion general de tipos de habitaciones.
    """
    try:
        rooms = get_rooms()
        if not rooms:
            return "No hay habitaciones registradas en el sistema."
        
        result = "Habitaciones del hotel \n\n"
        for room in rooms:
            result += f"-Habitaciones {room['numero']}: {room['tipo']} | "
            result += f"Precio: ${room['precio_noche']} | "
            result += f"Capacidad: {room['capacidad']} personas \n"

        return result
    except Exception as e:
        return f"Error al obtener habitaciones: {str(e)}"
    
@tool
def tool_get_available_rooms() -> str:
    """
    Retorn solo las habitaciones disponibles para reservar.
    úsalas cuando el usurio quiera hacer una reserva o consultar disponibilidad.
    """
    try:
        rooms = get_available_rooms()
        if not rooms:
            return "No hay habitaciones disponibles en este momento."
        result = "Habitaciones disponibles \n\n"

        for room in rooms:
            result += f" -ID: {room['id']} | habitación {room['numero']}: "
            result += f"{room['tipo']} | Precio: ${room['precio_noche']} / noche\n"
        
        return result 

    except Exception as e:
        return f" Error al consultar disponibilidad: {str(e)}"

@tool
def tool_create_reservation(
    id_number: str,
    name: str,
    room_id: int,
    checkin: str,
    checkout: str
) -> str:
    """
    Crea una reserva para un huésped.
    Úsala cuando el usuario quiera reservar una habitación.
    
    Args:
        id_number: Número de documento de identidad del huésped (cédula/pasaporte)
        name: Nombre completo del huésped
        room_id: ID de la habitación a reservar (obtenerlo de tool_get_available_rooms)
        checkin: Fecha de entrada en formato YYYY-MM-DD
        checkout: Fecha de salida en formato YYYY-MM-DD
    """
    try:
        # Validación básica de fechas antes de ir a la BD
        from datetime import datetime
        checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
        
        if checkout_date <= checkin_date:
            return " La fecha de salida debe ser posterior a la fecha de entrada."
        
        reserva = create_reservation(id_number, name, room_id, checkin, checkout)
        
        if reserva:
            return (
                f"Reserva creada exitosamente!\n"
                f"- ID Reserva: {reserva['id']}\n"
                f"- Huésped: {name}\n"
                f"- Habitación: {room_id}\n"
                f"- Check-in: {checkin}\n"
                f"- Check-out: {checkout}\n"
                f"- Estado: Pendiente"
            )
        return " No se pudo crear la reserva. Verifica los datos e intenta nuevamente."
    except ValueError:
        return " Formato de fecha incorrecto. Usa YYYY-MM-DD (ejemplo: 2025-12-01)"
    except Exception as e:
        return f"Error al crear reserva: {str(e)}"


@tool
def tool_get_reservations(id_number: str) -> str:
    """
    Consulta todas las reservas de un huésped por su número de documento.
    Úsala cuando el usuario quiera ver sus reservas activas o historial.
    
    Args:
        id_number: Número de documento de identidad del huésped
    """
    try:
        reservations = get_reservations_by_id(id_number)
        
        if not reservations:
            return f"No se encontraron reservas para el documento {id_number}."
        
        result = f" Reservas para documento {id_number}:\n\n"
        for res in reservations:
            result += f"- Reserva #{res['reserva_id']}: "
            result += f"Habitación {res['habitacion_id']} | "
            result += f"Check-in: {res['fecha_inicio']} | "
            result += f"Check-out: {res['fecha_fin']} | "
            result += f"Estado: {res['status']}\n"
        return result
    except Exception as e:
        return f"Error al consultar reservas: {str(e)}"


@tool
def tool_do_checkin(reserva_id: int) -> str:
    """
    Realiza el check-in de un huésped para una reserva existente.
    Úsala cuando el huésped llegue al hotel y quiera registrar su entrada.
    
    Args:
        reserva_id: ID numérico de la reserva
    """
    try:
        result = do_checkin(reserva_id)
        if result["success"]:
            return f" {result['message']}"
        return f" {result['message']}"
    except Exception as e:
        return f"Error en check-in: {str(e)}"


@tool
def tool_do_checkout(reserva_id: int) -> str:
    """
    Realiza el check-out de un huésped.
    Úsala cuando el huésped quiera registrar su salida del hotel.
    
    Args:
        reserva_id: ID numérico de la reserva
    """
    try:
        result = do_checkout(reserva_id)
        if result["success"]:
            return f" {result['message']}"
        return f" {result['message']}"
    except Exception as e:
        return f"Error en check-out: {str(e)}"


# Lista de tools para registrar en LangGraph
hotel_tools = [
    tool_get_hotel_info_rag,
    tool_get_rooms,
    tool_get_available_rooms,
    tool_create_reservation,
    tool_get_reservations,
    tool_do_checkin,
    tool_do_checkout
]