from flask import Flask, request, session, redirect, url_for, render_template, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super-insecure-secret'
DATABASE = 'database.db'
app.config.update(SESSION_COOKIE_HTTPONLY=False)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.context_processor
def inject_user():
    if 'user_id' in session:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (session['user_id'],))
        user = c.fetchone()
        if user:
            return dict(current_user=user[0])
    return dict(current_user=None)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    if 'user_id' in session:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id, username, name FROM users WHERE id != ?", (session['user_id'],))
        users = c.fetchall()
        return render_template('home.html', users=users)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, password, name))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, username, name FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    return render_template('profile.html', user=user)

@app.route('/follow/<int:user_id>')
def follow(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO follows (follower_id, followed_id) VALUES (?, ?)", (session['user_id'], user_id))
    db.commit()
    return redirect(url_for('notifications'))

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    c = db.cursor()
    c.execute('''
        SELECT users.name FROM follows
        JOIN users ON follows.follower_id = users.id
        WHERE follows.followed_id = ?
    ''', (session['user_id'],))
    followers = c.fetchall()
    return render_template('notifications.html', followers=followers)

if __name__ == '__main__':
    app.run(debug=True)
