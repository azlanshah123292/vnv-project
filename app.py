from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, DATABASE_NAME
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

def get_db():
    db_name = app.config.get('DATABASE', DATABASE_NAME)
    return get_db_connection(db_name)

@app.route('/')
def index():
    """Renders the home page with a list of all available rooms, optionally filtered by city."""
    city = request.args.get('city')
    conn = get_db()
    if city:
        rooms = conn.execute('SELECT * FROM rooms WHERE city = ?', (city,)).fetchall()
    else:
        rooms = conn.execute('SELECT * FROM rooms').fetchall()
    
    # Get all distinct cities for the dropdown
    cities = conn.execute('SELECT DISTINCT city FROM rooms WHERE city IS NOT NULL').fetchall()
    conn.close()
    return render_template('index.html', rooms=rooms, cities=cities, selected_city=city)

@app.route('/register', methods=('GET', 'POST'))
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        try:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs out the current user."""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """
    Renders the dashboard.
    Admins see all bookings.
    Users see their own bookings.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    if session['role'] == 'admin':
        bookings = conn.execute('''
            SELECT bookings.id, users.username, rooms.name, bookings.start_date, bookings.end_date, bookings.payment_method, bookings.payment_status 
            FROM bookings 
            JOIN users ON bookings.user_id = users.id 
            JOIN rooms ON bookings.room_id = rooms.id
        ''').fetchall()
        my_bookings = None
    else:
        bookings = None
        my_bookings = conn.execute('''
            SELECT bookings.id, rooms.name, bookings.start_date, bookings.end_date, bookings.payment_method, bookings.payment_status 
            FROM bookings 
            JOIN rooms ON bookings.room_id = rooms.id 
            WHERE bookings.user_id = ?
        ''', (session['user_id'],)).fetchall()
        
    conn.close()
    return render_template('dashboard.html', bookings=bookings, my_bookings=my_bookings)

@app.route('/add_room', methods=('GET', 'POST'))
def add_room():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']
        city = request.form['city']
        
        conn = get_db()
        conn.execute('INSERT INTO rooms (name, description, price, image_url, city) VALUES (?, ?, ?, ?, ?)',
                     (name, description, price, image_url, city))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    return render_template('add_room.html')

@app.route('/book/<int:room_id>', methods=('GET', 'POST'))
def book_room(room_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    room = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
    
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        payment_method = request.form['payment_method']
        
        payment_status = 'paid' if payment_method == 'card' else 'pending'
        
        conn.execute('INSERT INTO bookings (user_id, room_id, start_date, end_date, payment_method, payment_status) VALUES (?, ?, ?, ?, ?, ?)',
                     (session['user_id'], room_id, start_date, end_date, payment_method, payment_status))
        conn.commit()
        conn.close()
        flash('Room booked successfully!')
        return redirect(url_for('dashboard'))
        
    conn.close()
    return render_template('book_room.html', room=room)

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    # Check if booking belongs to user
    booking = conn.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,)).fetchone()
    if booking and (booking['user_id'] == session['user_id'] or session['role'] == 'admin'):
        conn.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        flash('Booking cancelled.')
    
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
