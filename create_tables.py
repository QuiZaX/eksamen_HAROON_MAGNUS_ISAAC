import sqlite3


def create_dynamic_tables(tournament_name):
    conn = sqlite3.connect('leaderboard.db')
    c = conn.cursor()

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS "{tournament_name}_groups" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            team_name TEXT NOT NULL
        )
    ''')

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS "{tournament_name}_matches" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            goals_team1 INTEGER NOT NULL,
            goals_team2 INTEGER NOT NULL,
            result TEXT NOT NULL,
            knockout INTEGER NOT NULL
        )
    ''')

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS "{tournament_name}_standings" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            team_name TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Example usage for dynamic tournaments
tournaments = ['gg', 'test1']
for tournament in tournaments:
    create_dynamic_tables(tournament)
