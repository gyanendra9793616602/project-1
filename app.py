from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('seeker', 'recruiter'))
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/save-details', methods=['POST'])
def save_details():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')

    # Server-side validation
    if not all([name, email, phone, role]) or role not in ['seeker', 'recruiter']:
        return jsonify({'success': False, 'message': 'Invalid input data.'}), 400

    # Email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({'success': False, 'message': 'Invalid email format.'}), 400

    # Phone validation (10 digits)
    phone_regex = r'^\d{10}$'
    if not re.match(phone_regex, phone):
        return jsonify({'success': False, 'message': 'Invalid phone number. Must be 10 digits.'}), 400

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, phone, role) VALUES (?, ?, ?, ?)',
                      (name, email, phone, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': user_id})
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Email or phone number already exists.'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Database error.'}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return jsonify({
            'success': True,
            'users': [
                {'id': user[0], 'name': user[1], 'email': user[2], 'phone': user[3], 'role': user[4]}
                for user in users
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Database error.'}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)