import sqlite3

def add_payment_columns():
    conn = sqlite3.connect('hotel.db')
    try:
        conn.execute("ALTER TABLE bookings ADD COLUMN payment_method TEXT DEFAULT 'hotel'")
        print("Successfully added 'payment_method' column to bookings table.")
    except sqlite3.OperationalError as e:
        print(f"Error adding 'payment_method': {e}")

    try:
        conn.execute("ALTER TABLE bookings ADD COLUMN payment_status TEXT DEFAULT 'pending'")
        print("Successfully added 'payment_status' column to bookings table.")
    except sqlite3.OperationalError as e:
        print(f"Error adding 'payment_status': {e}")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_payment_columns()
