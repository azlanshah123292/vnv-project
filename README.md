# Online Hotel Reservation System

A simple and effective Online Hotel Reservation System built using Python (Flask) and SQLite. This project allows users to browse rooms, book reservations, and view their booking history. It also includes an admin interface for managing rooms.

## Features

*   **User Authentication**: Secure registration and login system.
*   **Room Browsing**: View available rooms with images, descriptions, and prices.
*   **Booking System**: Simple interface to book rooms for specific dates.
*   **Dashboard**:
    *   **Users**: View personal booking history and cancel bookings.
    *   **Admins**: View all bookings and add new rooms to the system.
*   **Responsive Design**: Clean and clear user interface.

## Prerequisites

*   Python 3.x
*   Pip (Python Package Installer)

## Installation & Setup

1.  **Extract the project files** to a directory.

2.  **Open a terminal/command prompt** in the project folder.

3.  **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database**:
    ```bash
    python database.py
    ```
    This will create a `hotel.db` file in the directory.

5.  **Run the application**:
    ```bash
    python app.py
    ```

6.  **Access the website**:
    Open your web browser and go to `http://127.0.0.1:5000`

## Usage Guide

### Reviewers / Graders
To test the **Admin** features (Adding rooms, viewing all bookings), you need an admin account.
Since there is no "Create Admin" button for security, you can create one by modifying the database or using this simple script after registering a user (e.g., 'admin'):

```python
import sqlite3
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()
cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
conn.commit()
conn.close()
```

### Regular Users
1.  Register for a new account.
2.  Login with your credentials.
3.  Browse the "Available Rooms" on the home page.
4.  Click "Book Now", select dates, and confirm.
5.  Go to "Dashboard" to view your reservations.
