import sqlite3

DATABASE_NAME = 'hotel.db'

def update_admin_role():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("UPDATE users SET role = 'admin' WHERE username = 'user1'")
    conn.commit()
    conn.close()

def get_db_connection(db_name=DATABASE_NAME):
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_name=DATABASE_NAME):
    """Initializes the database with users, rooms, and bookings tables."""
    conn = get_db_connection(db_name)
    with conn:
        # Create Users Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        ''')
        
        # Create Rooms Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                city TEXT
            )
        ''')

        
        # Create Bookings Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                payment_method TEXT NOT NULL DEFAULT 'hotel',
                payment_status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (room_id) REFERENCES rooms (id)
            )
        ''')
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
