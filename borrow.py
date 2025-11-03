from flask import Blueprint, jsonify, session
from db import get_db_connection
from email_utils import send_email

borrow_bp = Blueprint('borrow', __name__, url_prefix='/borrow')

@borrow_bp.route('/book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    user_id = session.get('user_id')
    username = session.get('username')
    if not user_id:
        return jsonify({'error': 'Please log in first'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('borrow_book_proc', [user_id, book_id])
        conn.commit()

        cursor.execute("SELECT title FROM books WHERE id=%s", (book_id,))
        book = cursor.fetchone()

        subject = "Library Borrow Confirmation"
        body = f"Hi {username},\n\nYou have borrowed '{book['title']}'. Please return it within 14 days.\n\nHappy Reading!\nDigital Library"
        send_email(f"{username}@gmail.com", subject, body)

        return jsonify({'message': f"Book '{book['title']}' borrowed successfully! Confirmation email sent."})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()
