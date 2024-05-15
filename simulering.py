import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/45223/PycharmProjects/Eksamen/eksamen/teams.db')
cursor = conn.cursor()

# Fetch teams from the database
cursor.execute("SELECT name FROM teams")
teams_data = cursor.fetchall()

# Extract team names from the fetched data
teamlist = [team[0] for team in teams_data]

# Close the database connection
conn.close()

# Randomize teams at the start
random.shuffle(teamlist)
print("Teams randomized for initial seeding:", teamlist)

# Set defaults
gameid = 0

# Simulate all of the games
while len(teamlist) > 1:  # Loop until there's only one winner
    if gameid in [8, 12, 14]:  # This is a manual decision tree, doesn't scale at all
        # If a new round begins, reset the list of the next round
        print("--- Starting a new round of games ---")
        gameid = 0  # Reset gameid for the new round
        print("Next round matchup list:", teamlist)

    # Set roundid to 0 at the beginning of each round
    roundid = 0

    # Simulate games within the round
    while roundid < len(teamlist) - 1:  # Ensure roundid doesn't go out of range
        home_team = teamlist[roundid]
        away_team = teamlist[roundid + 1]

        # Input scores from admin for each team
        try:
            score_home = int(input(f"Enter the score for Team {home_team}: "))
            score_away = int(input(f"Enter the score for Team {away_team}: "))
        except ValueError:
            print("Invalid input. Please enter a valid integer score.")
            continue

        # Remove the losing team from the list
        if score_home > score_away:
            teamlist.remove(away_team)
            print(f"{home_team} vs {away_team}: The winner is {home_team}")
        else:
            teamlist.remove(home_team)
            print(f"{home_team} vs {away_team}: The winner is {away_team}")

        # Increase the roundid
        roundid += 2

    # Increase the gameid
    gameid += 1

# Output the final winner
print("Champion is:", teamlist[0])
