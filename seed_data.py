import sqlite3
from database import get_db_connection

def seed_rooms():
    conn = get_db_connection()
    
    cities = ["Hunza", "Skardu", "Murree", "Swat"]
    
    room_types = [
        {
            "name": "Luxury Suite",
            "description": "Experience ultimate comfort with a king-sized bed, private balcony, jacuzzi, and complimentary breakfast at Azlan Heights.",
            "price": 30000.00,
            "image_url": "/static/images/luxury_suite.jpg"
        },
        {
            "name": "Standard Double",
            "description": "A comfortable room with a double bed, suitable for couples. Includes flat-screen TV, free Wi-Fi, and a city view.",
            "price": 20000.00,
            "image_url": "/static/images/standard_double.jpg"
        },
        {
            "name": "Economy Single",
            "description": "A cozy and affordable room with a single bed, work desk, and modern amenities. Ideal for solo travelers on a budget.",
            "price": 10000.00,
            "image_url": "/static/images/economy_single.jpg"
        }
    ]

    print("Re-seeding database for Azlan Heights branches...")
    
    # Optional: Clear existing rooms to avoid duplicates/confusion with old data
    conn.execute('DELETE FROM rooms')
    print("Cleared existing rooms data.")

    for city in cities:
        print(f"Adding rooms for Azlan Heights - {city} Branch...")
        for room in room_types:
            conn.execute('INSERT INTO rooms (name, description, price, image_url, city) VALUES (?, ?, ?, ?, ?)',
                         (room['name'], room['description'], room['price'], room['image_url'], city))
            print(f"  Added: {room['name']}")

    conn.commit()
    conn.close()
    print("Database seeding completed.")

if __name__ == '__main__':
    seed_rooms()
