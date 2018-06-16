# -*- coding: utf-8 -*-
import sqlite3
from conf import DB_NAME


if __name__ == '__main__':
    db_connection = sqlite3.connect(DB_NAME)
    cursor = db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY,
        username VARCHAR,
        first_name VARCHAR,
        last_name VARCHAR,
        type VARCHAR,
        created_at integer(4) not null default (strftime('%s','now'))
    )''')
    db_connection.commit()
    db_connection.close()
