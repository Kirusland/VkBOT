import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (user_id INTEGER PRIMARY KEY)
''')

def write_user_id(user_id):
    cursor.execute('''
    INSERT INTO users (user_id) VALUES (?)
    ''', (user_id,))

    conn.commit()

def delete_user_id(user_id):
    cursor.execute('''
        DELETE FROM users WHERE user_id = ?
    ''', (user_id,))
    conn.commit()

def read_all_user_ids():
    cursor.execute('''
        SELECT user_id FROM users
    ''')
    return [row for row in cursor.fetchall()]

all_user_ids = read_all_user_ids()


def check_user_id(user_id):
    if (user_id,) in all_user_ids:
        return(True)
    else:
        return(False)
