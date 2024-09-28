from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import hashlib
import jwt
import datetime

app = Flask(__name__)
CORS(app)
SECRET_KEY = 'your_secret_key'

DATABASE = 'health_diary.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL,
                    height INTEGER,
                    blood_group TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    blood_sugar REAL,
                    weight REAL,
                    temperature REAL,
                    pulse INTEGER,
                    pressure TEXT,
                    overall_state INTEGER,
                    oxygen_level REAL,
                    cholesterol REAL,
                    date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_jwt_token(user_id):
    token = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
    return token


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def user_exists_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user is not None


def user_exists_by_login(login):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
    conn.close()
    return user is not None


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    login = data['login']
    password = hash_password(data['password'])
    name = data['name']
    height = data.get('height')
    blood_group = data.get('blood_group')

    if user_exists_by_login(login):
        return jsonify({'error': 'User already exists'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (login, password, name, height, blood_group) VALUES (?, ?, ?, ?, ?)', 
                   (login, password, name, height, blood_group))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    token = generate_jwt_token(user_id)
    return jsonify({'id': user_id, 'login': login, 'token': token})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data['login']
    password = hash_password(data['password'])

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'Invalid login or password'}), 400

    token = generate_jwt_token(user['id'])
    return jsonify({'id': user['id'], 'login': user['login'], 'token': token})


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return jsonify(dict(user))


@app.route('/user/login/<login>', methods=['GET'])
def get_user_by_login(login):
    if not user_exists_by_login(login):
        return jsonify({'error': 'User not found'}), 404

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
    conn.close()
    return jsonify(dict(user))


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.execute('DELETE FROM statistics WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully'})


@app.route('/statistics', methods=['POST'])
def add_statistics():
    data = request.json
    user_id = data['user_id']
    blood_sugar = data['blood_sugar']
    weight = data['weight']
    temperature = data['temperature']
    pulse = data['pulse']
    pressure = data['pressure']
    overall_state = data['overall_state']
    oxygen_level = data['oxygen_level']
    cholesterol = data['cholesterol']
    date = datetime.date.today().strftime("%Y-%m-%d")

    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    conn = get_db_connection()
    conn.execute('''INSERT INTO statistics 
                    (user_id, blood_sugar, weight, temperature, pulse, pressure, overall_state, oxygen_level, cholesterol, date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (user_id, blood_sugar, weight, temperature, pulse, pressure, overall_state, oxygen_level, cholesterol, date))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Statistics added successfully'})


@app.route('/statistics/day/<int:user_id>', methods=['GET'])
def get_statistics_by_day(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    date = datetime.date.today().strftime("%Y-%m-%d")
    conn = get_db_connection()
    stats = conn.execute('SELECT * FROM statistics WHERE user_id = ? AND date = ?', (user_id, date)).fetchall()
    conn.close()

    return jsonify([dict(stat) for stat in stats])


@app.route('/statistics/week/<int:user_id>', methods=['GET'])
def get_statistics_by_week(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=7)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    conn = get_db_connection()
    stats = conn.execute('SELECT * FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ?', (user_id, start_date, end_date)).fetchall()
    conn.close()

    return jsonify([dict(stat) for stat in stats])


@app.route('/statistics/month/<int:user_id>', methods=['GET'])
def get_statistics_by_month(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    start_date = datetime.date.today()
    end_date = (start_date + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    conn = get_db_connection()
    stats = conn.execute('SELECT * FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ?', (user_id, start_date, end_date)).fetchall()
    conn.close()

    return jsonify([dict(stat) for stat in stats])


@app.route('/statistics/year/<int:user_id>', methods=['GET'])
def get_statistics_by_year(user_id):
    if not user_exists_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    start_date = datetime.date.today()
    end_date = (start_date + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")

    conn = get_db_connection()
    stats = conn.execute('SELECT * FROM statistics WHERE user_id = ? AND date BETWEEN ? AND ?', (user_id, start_date, end_date)).fetchall()
    conn.close()

    return jsonify([dict(stat) for stat in stats])


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000)
