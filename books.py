from flask import Blueprint, render_template, request, jsonify, session
from db import get_db_connection

books_bp = Blueprint('books', __name__, url_prefix='/books')

# ---------- SEARCH & DISPLAY ----------
@books_bp.route('/list')
def list_books():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if query:
        cursor.execute("""
            SELECT b.id, b.title, b.author, c.name AS category_name, b.available_copies
            FROM books b
            JOIN categories c ON b.category_id = c.id
            WHERE LOWER(b.title) LIKE %s OR LOWER(b.author) LIKE %s OR LOWER(c.name) LIKE %s
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM book_view")

    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(books)

# ---------- ADMIN: ADD BOOK ----------
@books_bp.route('/add', methods=['POST'])
def add_book():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    title = data.get('title')
    author = data.get('author')
    category_id = data.get('category_id')
    copies = data.get('available_copies', 1)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, category_id, available_copies) VALUES (%s, %s, %s, %s)",
                   (title, author, category_id, copies))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f"Book '{title}' added successfully!"})

# ---------- ADMIN: DELETE BOOK ----------
@books_bp.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f"Book ID {book_id} deleted."})

# ---------- ADMIN: UPDATE BOOK ----------
@books_bp.route('/update/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    title = data.get('title')
    author = data.get('author')
    category_id = data.get('category_id')
    copies = data.get('available_copies')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books SET title=%s, author=%s, category_id=%s, available_copies=%s
        WHERE id=%s
    """, (title, author, category_id, copies, book_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f"Book ID {book_id} updated."})
