from app.database.database import get_connection
from datetime import datetime



class FinanceModel:

    @staticmethod
    def total_revenue():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT IFNULL(SUM(s.price), 0)
            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def today_revenue():

        today = datetime.now().strftime("%d/%m/%Y")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT IFNULL(SUM(s.price), 0)

            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'
            AND a.appointment_date = ?
        """, (today,))

        total = cursor.fetchone()[0]

        conn.close()

        return total

    @staticmethod
    def paid_appointments():

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
    def barber_report():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                u.username AS barber,
                COUNT(a.id) AS appointments,
                IFNULL(SUM(s.price), 0) AS total

            FROM appointments a

            JOIN users u
                ON u.id = a.barber_id

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            GROUP BY u.username

            ORDER BY total DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    @staticmethod
    def last_payments():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.appointment_date,
                c.name,
                s.price

            FROM appointments a

            JOIN clients c
                ON c.id = a.client_id

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            ORDER BY a.id DESC

            LIMIT 20
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    

    @staticmethod
    def monthly_revenue():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                substr(a.appointment_date, 6, 2) AS month,
                IFNULL(SUM(s.price), 0) AS total

            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            GROUP BY month

            ORDER BY month
        """)

        data = cursor.fetchall()

        conn.close()

        return data
    

    @staticmethod
    def top_services():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.name AS service,
                COUNT(a.id) AS total

            FROM appointments a

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            GROUP BY s.name

            ORDER BY total DESC

            LIMIT 5
        """)

        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def barber_revenue():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                u.username AS barber,
                IFNULL(SUM(s.price), 0) AS total

            FROM appointments a

            JOIN users u
                ON u.id = a.barber_id

            JOIN services s
                ON s.id = a.service_id

            WHERE a.status = 'Pago'

            GROUP BY u.username

            ORDER BY total DESC
        """)

        data = cursor.fetchall()

        conn.close()

        return data