import sqlite3
import random
import math

# Prompt the user to enter the tournament name
tournament_name = input("Enter the tournament name: ").replace(" ", "_")

# Connect to the SQLite database for teams
conn = sqlite3.connect('C:/Users/45223/PycharmProjects/Eksamen/eksamen/teams.db')
cursor = conn.cursor()

# Fetch teams from the 'selected_teams' table in the database
cursor.execute("SELECT name FROM selected_teams")
teams_data = cursor.fetchall()

# Extract team names from the fetched data
teams = [team[0] for team in teams_data]

# Display the teams in the tournament
print("Teams in the tournament:")
for team in teams:
    print(team)
print()  # Newline for better readability

# Close the database connection
conn.close()

# Randomize teams
random.shuffle(teams)

# Connect to the SQLite database for the leaderboard
conn = sqlite3.connect('leaderboard.db')
cursor = conn.cursor()

# Create tables for the tournament
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS "{tournament_name}_groups" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    team_name TEXT
)
""")
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS "{tournament_name}_matches" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    team1 TEXT,
    team2 TEXT,
    goals_team1 INTEGER,
    goals_team2 INTEGER,
    result TEXT,
    knockout INTEGER
)
""")
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS "{tournament_name}_standings" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    team_name TEXT,
    points INTEGER
)
""")

# Function to play a match
def play_match(group_name, team1, team2, knockout=False):
    print(f"Match: {team1} vs {team2}")
    valid_result = False
    while not valid_result:
        try:
            goals_team1 = int(input(f"Enter goals for {team1}: "))
            goals_team2 = int(input(f"Enter goals for {team2}: "))
            valid_result = True
        except ValueError:
            print("Invalid input. Please enter a valid number of goals.")

    result = ''
    if goals_team1 > goals_team2:
        winner = team1
        result = f"{team1} wins"
    elif goals_team1 < goals_team2:
        winner = team2
        result = f"{team2} wins"
    else:
        result = "Draw"
        if knockout:
            print(f"The match is a draw. Proceeding to penalties: {team1} vs {team2}")
            valid_result = False
            while not valid_result:
                try:
                    penalties_team1 = int(input(f"Enter penalty goals for {team1}: "))
                    penalties_team2 = int(input(f"Enter penalty goals for {team2}: "))
                    valid_result = True
                except ValueError:
                    print("Invalid input. Please enter a valid number of penalty goals.")
            if penalties_team1 > penalties_team2:
                winner = team1
                result = f"{team1} wins in penalties"
            else:
                winner = team2
                result = f"{team2} wins in penalties"

    cursor.execute(
        f'INSERT INTO "{tournament_name}_matches" (group_name, team1, team2, goals_team1, goals_team2, result, knockout) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (group_name, team1, team2, goals_team1, goals_team2, result, int(knockout))
    )
    conn.commit()

    if knockout:
        return winner
    else:
        if goals_team1 > goals_team2:
            return {team1: 3, team2: 0}
        elif goals_team1 < goals_team2:
            return {team1: 0, team2: 3}
        else:
            return {team1: 1, team2: 1}

if len(teams) >= 8:
    # Calculate the number of groups (each group will have 4 teams)
    num_groups = math.ceil(len(teams) / 4)
    groups = [teams[i * 4:(i + 1) * 4] for i in range(num_groups)]

    # Insert groups and teams into the database
    for index, group in enumerate(groups):
        group_name = f"Group {index + 1}"
        for team in group:
            cursor.execute(f'INSERT INTO "{tournament_name}_groups" (group_name, team_name) VALUES (?, ?)',
                           (group_name, team))
    conn.commit()

    # Simulate all matches in each group and calculate points
    group_results = {}
    for index, group in enumerate(groups):
        standings = {team: 0 for team in group}
        group_name = f"Group {index + 1}"
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                result = play_match(group_name, group[i], group[j])
                standings[group[i]] += result[group[i]]
                standings[group[j]] += result[group[j]]
                # Display standings after each match
                sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
                print(f"Group {index + 1} Standings after {group[i]} vs {group[j]}:")
                for pos, (team, points) in enumerate(sorted_standings):
                    print(f"{pos + 1}: {team} with {points} points")
                print()  # Newline for better readability
        group_results[group_name] = sorted_standings

    # Insert final standings into the database
    for group, results in group_results.items():
        for pos, (team, points) in enumerate(results):
            cursor.execute(f'INSERT INTO "{tournament_name}_standings" (group_name, team_name, points) VALUES (?, ?, ?)',
                           (group, team, points))
    conn.commit()

    # Display the final standings for each group
    for group, results in group_results.items():
        print(f"{group} Final Standings:")
        for pos, (team, points) in enumerate(results):
            print(f"{pos + 1}: {team} with {points} points")
        print()  # Newline for better readability

    # Prepare teams for the knockout stage
    qualified_teams = []
    for group, results in group_results.items():
        qualified_teams.append(results[0][0])  # Top team
        if len(results) > 1:
            qualified_teams.append(results[1][0])  # Second top team

    # Display teams qualified for the knockout stage
    print("Teams qualified for the knockout stage:")
    print(", ".join(qualified_teams))
    print()  # Newline for better readability

else:
    # Directly proceed to knockout stage
    qualified_teams = teams

# Randomize teams for knockout stage
random.shuffle(qualified_teams)
print("Teams randomized for knockout stage seeding:", qualified_teams)

# Simulate knockout stage
while len(qualified_teams) > 1:
    next_round_teams = []
    print("--- Starting a new knockout round ---")
    for i in range(0, len(qualified_teams), 2):
        if i + 1 < len(qualified_teams):
            team1 = qualified_teams[i]
            team2 = qualified_teams[i + 1]
            winner = play_match('Knockout', team1, team2, knockout=True)
            next_round_teams.append(winner)
        else:
            next_round_teams.append(qualified_teams[i])
            print(f"{qualified_teams[i]} advances to the next round automatically.")
    qualified_teams = next_round_teams

# Output the final winner
print("Champion is:", qualified_teams[0])

# Close the database connection
conn.close()
