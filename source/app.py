from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets
import os
import time
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL)''')
    
    admin_exists = c.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exists:
        admin_hash = generate_password_hash('super_secret_admin_password_12345')
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                  ('admin', admin_hash))
    
    conn.commit()
    conn.close()

TOKEN_TTL_SECONDS = 300
app.config["LOGIN_TOKENS"] = {}

def hash_token(token):
    token_bytes = token.encode("utf-8")
    hasher = hashlib.sha256()
    hasher.update(token_bytes)
    return hasher.hexdigest()

def store_auth_token(token):
    token_hash = hash_token(token)
    expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    app.config["LOGIN_TOKENS"][token_hash] = (expires_at)

def consume_auth_token(token):
    token_hash = hash_token(token)
    now = int(time.time())

    entry = app.config["LOGIN_TOKENS"][token_hash]
    if not entry:
        return False

    expires_at = entry
    if expires_at < now:
        return False

    return True

file_path = "app.db"

if os.path.exists(file_path):
    os.remove(file_path)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    
    try:
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  (username, password_hash))
        conn.commit()
        user_id = c.lastrowid
        return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        conn.close()

@app.route('/api/login/verify', methods=['POST'])
def login_verify():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    user = c.execute('SELECT id, password_hash FROM users WHERE username = ?',
                     (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        token = secrets.token_urlsafe(32)
        store_auth_token(token)
        return jsonify({
            'message': 'Credentials verified',
            'user_id': user[0],
            'token': token
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/login/session', methods=['POST'])
def login_session():
    auth_header = request.headers.get('Authorization')
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing authorization token'}), 401
    
    token = auth_header.split(" ")[1].strip()
    
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401

    if not user_id:
        return jsonify({'error': 'User ID required'}), 400

    if not consume_auth_token(token):
        return jsonify({"error": "Invalid or expired token"}), 401
    
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    user = c.execute('SELECT id, username FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    session['user_id'] = user[0]
    session['username'] = user[1]
    
    if user[1] == 'admin':
        return jsonify({
            'message': 'Login successful',
            'username': user[1],
            'flag': 'ATHACKCTF{1n53cur3_d1r3c7_4l13n_r3f3r3nc3}'
        }), 200
    
    return jsonify({
        'message': 'Login successful',
        'username': user[1]
    }), 200

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)