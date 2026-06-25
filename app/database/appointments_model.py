from app.database.database import get_connection
from datetime import datetime

class AppointmentsModel:

    @staticmethod
    def create_table():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                barber_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT DEFAULT 'Agendado',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(client_id)
                    REFERENCES clients(id),

                FOREIGN KEY(service_id)
                    REFERENCES services(id),

                FOREIGN KEY(barber_id)
                    REFERENCES users(id)
            )
        """)

        conn.commit()
        conn.close()


    @staticmethod
    def get_all():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.id,
                c.name AS client,
                s.name AS service,
                s.price,
                u.username AS barber,
                a.appointment_date,
                a.appointment_time,
                a.status
            FROM appointments a

            JOIN clients c
                ON c.id = a.client_id

            JOIN services s
                ON s.id = a.service_id

            JOIN users u
                ON u.id = a.barber_id

            ORDER BY a.appointment_date,
                     a.appointment_time
        """)

        appointments = cursor.fetchall()

        conn.close()

        return appointments
    

    @staticmethod
    def create(
        client_id,
        service_id,
        barber_id,
        date,
        time
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO appointments (
                client_id,
                service_id,
                barber_id,
                appointment_date,
                appointment_time
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            client_id,
            service_id,
            barber_id,
            date,
            time
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def delete(appointment_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM appointments WHERE id = ?",
            (appointment_id,)
        )

        conn.commit()
        conn.close()


    
    @staticmethod
    def get_by_id(appointment_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM appointments
            WHERE id = ?
        """, (
            appointment_id,
        ))

        appointment = cursor.fetchone()

        conn.close()

        return appointment
    

    @staticmethod
    def update(
        appointment_id,
        client_id,
        service_id,
        barber_id,
        date,
        time,
        status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE appointments
            SET
                client_id = ?,
                service_id = ?,
                barber_id = ?,
                appointment_date = ?,
                appointment_time = ?,
                status = ?
            WHERE id = ?
        """, (
            client_id,
            service_id,
            barber_id,
            date,
            time,
            status,
            appointment_id
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total
    

    @staticmethod
    def update_status(appointment_id, status):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE appointments
            SET status = ?
            WHERE id = ?
        """, (
            status,
            appointment_id
        ))

        conn.commit()
        conn.close()


    
    @staticmethod
    def get_paid():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.appointment_date,
                c.name,
                s.name,
                s.price
            FROM appointments a

            JOIN clients c
                ON c.id = a.client_id

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            ORDER BY a.appointment_date DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def total_paid():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(s.price)

            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total or 0


    @staticmethod
    def paid_count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM appointments
            WHERE status = 'Pago'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    

    @staticmethod
    def finished_count():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM appointments
            WHERE status = 'Concluído'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    

    @staticmethod
    def exists(barber_id, date, time):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM appointments
            WHERE barber_id = ?
            AND appointment_date = ?
            AND appointment_time = ?
            AND status != 'Cancelado'
        """, (
            barber_id,
            date,
            time
        ))

        exists = cursor.fetchone()

        conn.close()

        return exists is not None
    

    @staticmethod
    def today():

        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.appointment_time,
                c.name AS client,
                u.username AS barber,
                a.status

            FROM appointments a

            JOIN clients c
                ON c.id = a.client_id

            JOIN users u
                ON u.id = a.barber_id

            WHERE a.appointment_date = ?

            ORDER BY a.appointment_time
        """, (today,))

        data = cursor.fetchall()

        conn.close()

        return data