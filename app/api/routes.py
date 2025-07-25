from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from models.user_model import get_db, user_to_dict
from utils.validators import validate_user_data
import sqlite3

api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        db = get_db()
        users = db.execute('SELECT * FROM users').fetchall()
        return jsonify([user_to_dict(u) for u in users]), 200
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

@api_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            return jsonify(user_to_dict(user)), 200
        return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

@api_bp.route('/users', methods=['POST'])  # Signup route – keep public
def create_user():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid or malformed JSON'}), 400

    errors = validate_user_data(data, require_password=True)
    if errors:
        return jsonify(errors), 400

    try:
        db = get_db()
        hashed_password = generate_password_hash(data['password'])
        db.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (data['name'], data['email'], hashed_password)
        )
        db.commit()
        return jsonify({'message': 'User created'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Email already exists', 'details': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'User creation failed', 'details': str(e)}), 500

@api_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid or malformed JSON'}), 400

    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Invalid data: name and email required'}), 400

    try:
        db = get_db()
        db.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (data['name'], data['email'], user_id)
        )
        db.commit()
        return jsonify({'message': 'User updated'}), 200
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'Email already exists', 'details': str(e)}), 409
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

@api_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        db = get_db()
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
        return jsonify({'message': f'User {user_id} deleted'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

@api_bp.route('/search', methods=['GET'])
@jwt_required()
def search_user():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Provide a name'}), 400

    try:
        db = get_db()
        users = db.execute(
            "SELECT * FROM users WHERE name LIKE ?", (f'%{name}%',)
        ).fetchall()
        return jsonify([user_to_dict(u) for u in users]), 200
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
