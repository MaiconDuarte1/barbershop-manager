import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "barbershop.db"
)


def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn