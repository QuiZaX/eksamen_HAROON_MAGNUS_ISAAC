from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Generate a secret key for Flask sessions

# Function to create database tables
def create_tables():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Function to add user to the database
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    conn.close()

# Function to check if user exists
def user_exists(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?''', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Function to save team name into the database
def save_team_name(team_name):
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    c.execute('''INSERT INTO teams (name) VALUES (?)''', (team_name,))
    conn.commit()
    conn.close()

# Function to fetch team names from the database
def get_team_names():
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    c.execute('''SELECT name FROM teams''')
    teams = c.fetchall()
    conn.close()
    return teams

# Endpoint to fetch team names
@app.route('/get_teams')
def get_teams():
    teams = get_team_names()
    print("Teams retrieved from database:", teams)  # Debugging statement
    return jsonify([{'name': team[0]} for team in teams])

@app.route('/')
def index():
    session.clear()  # Clear session data
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_exists(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/save_team', methods=['POST'])
def save_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        try:
            save_team_name(team_name)
            return 'Team name saved successfully!'
        except Exception as e:
            return f'An error occurred: {str(e)}'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/turnering')
def turnering():
    return render_template('turnering.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

if __name__ == '__main__':
    create_tables()  # Create database tables if they don't exist
    app.run(debug=True)
