import sqlite3

# Function to create dynamic tables for a given tournament
def create_dynamic_tables(tournament_name):
    conn = sqlite3.connect('tournaments.db')
    c = conn.cursor()

    # Create groups table
    c.execute(f'''CREATE TABLE IF NOT EXISTS {tournament_name}_groups (
                    id INTEGER PRIMARY KEY,
                    group_name TEXT)''')

    # Create matches table
    c.execute(f'''CREATE TABLE IF NOT EXISTS {tournament_name}_matches (
                    id INTEGER PRIMARY KEY,
                    match_name TEXT)''')

    # Create standings table
    c.execute(f'''CREATE TABLE IF NOT EXISTS {tournament_name}_standings (
                    id INTEGER PRIMARY KEY,
                    team_name TEXT,
                    points INTEGER)''')

    conn.commit()
    conn.close()
