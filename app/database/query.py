from connection import get_connection


def get_rooms():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM habitaciones")
            return cur.fetchall()
        

if __name__=='__main__':
    rooms = get_rooms()
    print(rooms)