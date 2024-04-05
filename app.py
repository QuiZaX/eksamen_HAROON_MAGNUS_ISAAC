from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # You should generate a secret key for Flask sessions

# Function to create database
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Function to add user to the database
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

# Function to check if the user exists
def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    user = c.fetchone()
    conn.close()
    return user is not None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if user_exists(username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''SELECT password FROM users WHERE username = ?''', (username,))
        stored_password = c.fetchone()[0]
        conn.close()
        if password == stored_password:
            session['username'] = username  # Store username in session
            return redirect(url_for('home', username=username))  # Redirect to home page
        else:
            return "Incorrect password. Please try again."
    else:
        return "User does not exist. Please register first."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not user_exists(username):
            add_user(username, password)
            return redirect(url_for('index'))
        else:
            return "User already exists. Please choose another username."
    return render_template('register.html')

@app.route('/success/<username>')
def success(username):
    return f"Welcome {username}!"

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('index'))

@app.route('/login_success')
def login_success():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('home', username=username))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    create_table()  # Create the database table if it doesn't exist
    app.run(debug=True)
