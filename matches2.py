import sqlite3
import random
import math

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/45223/PycharmProjects/Eksamen/eksamen/teams.db')
cursor = conn.cursor()

# Fetch teams from the database
cursor.execute("SELECT name FROM teams")
teams_data = cursor.fetchall()

# Extract team names from the fetched data
teams = [team[0] for team in teams_data]

# Close the database connection
conn.close()

# Randomize teams
random.shuffle(teams)

# Calculate the number of groups (each group will have 4 teams)
num_groups = math.ceil(len(teams) / 4)
groups = [teams[i * 4:(i + 1) * 4] for i in range(num_groups)]

# Display all teams before the matches begin
print("Teams and Groups before matches begin:")
for index, group in enumerate(groups):
    print(f"Group {index + 1}: {', '.join(group)}")
print()  # Newline for better readability

# Function to allow admin to input match results
def play_match(team1, team2, knockout=False):
    print(f"Match: {team1} vs {team2}")
    valid_result = False
    while not valid_result:
        try:
            goals_team1 = int(input(f"Enter goals for {team1}: "))
            goals_team2 = int(input(f"Enter goals for {team2}: "))
            valid_result = True
        except ValueError:
            print("Invalid input. Please enter a valid number of goals.")

    if goals_team1 > goals_team2:
        winner = team1
        if knockout:
            return winner
        else:
            return {team1: 3, team2: 0}
    elif goals_team1 < goals_team2:
        winner = team2
        if knockout:
            return winner
        else:
            return {team1: 0, team2: 3}
    else:
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
                print(f"{team1} wins in penalties and advances.")
            else:
                winner = team2
                print(f"{team2} wins in penalties and advances.")
            return winner
        else:
            return {team1: 1, team2: 1}

# Simulate all matches in each group and calculate points
group_results = {}
for index, group in enumerate(groups):
    standings = {team: 0 for team in group}
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            result = play_match(group[i], group[j])
            standings[group[i]] += result[group[i]]
            standings[group[j]] += result[group[j]]
            # Display standings after each match
            sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
            print(f"Group {index + 1} Standings after {group[i]} vs {group[j]}:")
            for pos, (team, points) in enumerate(sorted_standings):
                print(f"{pos + 1}: {team} with {points} points")
            print()  # Newline for better readability
    group_results[f'Group {index + 1}'] = sorted_standings

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
            winner = play_match(team1, team2, knockout=True)
            next_round_teams.append(winner)
        else:
            next_round_teams.append(qualified_teams[i])
            print(f"{qualified_teams[i]} advances to the next round automatically.")
    qualified_teams = next_round_teams

# Output the final winner
print("Champion is:", qualified_teams[0])
