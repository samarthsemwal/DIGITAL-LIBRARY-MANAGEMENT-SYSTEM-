from flask import Flask, render_template, request, session, redirect, url_for
from db import get_db_connection
from borrow import borrow_bp
from chatbot import chatbot_bp
from books import books_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(borrow_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(books_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role', 'user')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
                       (username, password, role))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('admin_dashboard' if role == 'admin' else 'dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials", role=role)
    return render_template('login.html', role=role)

@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'user':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM book_view")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', username=session['username'], books=books)

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM borrow_records")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', username=session['username'], records=records)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

