import os.path
import sqlite3
import resources
import bank


def create_connection():
    if os.path.isfile(resources.DB_FILENAME):
        return sqlite3.connect(resources.DB_FILENAME)
    conn = sqlite3.connect(resources.DB_FILENAME)
    cur = conn.cursor()
    cur.execute(resources.DB_CREATE_TABLE.strip())
    conn.commit()
    return conn


def main():
    conn = create_connection()
    bank.Bank(conn).main_menu()


if __name__ == '__main__':
    main()
