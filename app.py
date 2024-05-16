from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Generate a secret key for Flask sessions

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to create initial database tables (users and teams)
def create_initial_tables():
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
    c.execute('''SELECT id, name FROM teams''')
    teams = c.fetchall()
    conn.close()
    return teams

# Function to create a new table for selected teams
def create_selected_teams_table():
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS selected_teams (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Function to save selected teams into the new table
def save_selected_teams_to_db(selected_teams):
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    c.execute('DELETE FROM selected_teams')  # Clear previous selections
    for i, team_id in enumerate(selected_teams):
        team_name = f"team {i + 1}"
        c.execute('INSERT INTO selected_teams (id, name) VALUES (?, ?)', (team_id, team_name))
    conn.commit()
    conn.close()

@app.route('/get_teams')
def get_teams():
    teams = get_team_names()
    return jsonify([{'id': team[0], 'name': team[1]} for team in teams])

@app.route('/save_selected_teams', methods=['POST'])
def save_selected_teams():
    selected_teams = request.json.get('selected_teams', [])
    try:
        create_selected_teams_table()
        save_selected_teams_to_db(selected_teams)
        return jsonify({'message': 'Teams saved successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    team_name = request.form['team_name']
    try:
        save_team_name(team_name)
        return jsonify({'message': 'Team name saved successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/matches', methods=['GET', 'POST'])
def matches():
    tournament_name = request.args.get('tournament_name')
    tournament_names = get_tournament_names()  # Fetch tournament names

    if request.method == 'POST':
        tournament_name = request.form.get('tournament_name')
        return redirect(url_for('matches', tournament_name=tournament_name))

    if not tournament_name:
        return render_template('matches.html', tournament_name=None, groups_data=None, matches_data=None,
                               standings_data=None, champion=None, tournaments=tournament_names)

    create_dynamic_tables(tournament_name)  # Ensure tables are created for the tournament
    groups_data = get_groups_data(tournament_name)
    matches_data, champion = get_matches_data(tournament_name)
    standings_data = get_leaderboard_data(tournament_name)
    logging.debug(f"Standings data to render: {standings_data}")
    logging.debug(f"Champion: {champion}")
    return render_template('matches.html', tournament_name=tournament_name, groups_data=groups_data,
                           matches_data=matches_data, standings_data=standings_data, champion=champion,
                           tournaments=tournament_names)

if __name__ == '__main__':
    create_initial_tables()  # Create initial user and teams database tables if they don't exist
    app.run(debug=True)
