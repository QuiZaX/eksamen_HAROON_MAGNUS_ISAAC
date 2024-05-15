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

# In a single elimination tournament with a full field, the number of games is the number of teams - 1
totalgames = len(teamlist) - 1

# Set defaults
gameid = 0
roundid = 0
nextround = []

# Simulate all of the games
while gameid < totalgames:
    if gameid in [8, 12, 14]:  # This is a manual decision tree, doesn't scale at all
        # If a new round begins, reset the list of the next round
        print("--- Starting a new round of games ---")
        teamlist = nextround
        nextround = []
        roundid = 0

    # Compare the 1st entry in the list to the 2nd entry in the list
    home_team = teamlist[roundid]
    away_team = teamlist[roundid + 1]

    # Input scores from admin for each team
    score_home = int(input(f"Enter the score for Team {home_team}: "))
    score_away = int(input(f"Enter the score for Team {away_team}: "))

    # The winner of the match becomes the next entry in the nextround list
    if score_home > score_away:
        nextround.append(home_team)
        print(f"{home_team} vs {away_team}: The winner is {home_team}")
    else:
        nextround.append(away_team)
        print(f"{home_team} vs {away_team}: The winner is {away_team}")

    # Increase the gameid and roundid
    gameid += 1
    roundid += 2
    print("Next round matchup list:", nextround)

# Output the final winner
print("Champion is:", nextround[0])
