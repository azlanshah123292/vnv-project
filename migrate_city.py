import sqlite3

def add_city_column():
    conn = sqlite3.connect('hotel.db')
    try:
        conn.execute('ALTER TABLE rooms ADD COLUMN city TEXT')
        print("Successfully added 'city' column to rooms table.")
    except sqlite3.OperationalError:
        print("'city' column already exists.")
    finally:
        conn.close()

if __name__ == '__main__':
    add_city_column()
