from flask import Flask, render_template, request

app = Flask(__name__)

def simulate_match(team1, team2):
    """Simulerer en fodboldkamp mellem to hold."""
    # Her kan du ændre til at simulere kampene baseret på dine ønsker
    score_team1 = 1
    score_team2 = 2
    return score_team1, score_team2

def simulate_tournament(teams):
    """Simulerer en fodboldturnering mellem en liste af hold."""
    # Simuler turneringen baseret på antallet af hold
    standings = {team: 0 for team in teams}  # Opretter et tomt resultatopstilling
    for i, team1 in enumerate(teams):
        for j, team2 in enumerate(teams):
            if i < j:  # Simulerer kun hver kamp én gang (undgår at gentage kampe)
                score_team1, score_team2 = simulate_match(team1, team2)
                if score_team1 > score_team2:
                    standings[team1] += 3  # 3 point for sejr
                elif score_team1 < score_team2:
                    standings[team2] += 3  # 3 point for sejr
                else:
                    standings[team1] += 1  # 1 point for uafgjort
                    standings[team2] += 1  # 1 point for uafgjort
    sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
    return sorted_standings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournament_results', methods=['POST'])
def tournament_results():
    num_teams = int(request.form['num_teams'])
    teams = [request.form[f'team{i+1}'] for i in range(num_teams)]
    tournament_results = simulate_tournament(teams)
    return render_template('tournament_results.html', tournament_results=tournament_results)

if __name__ == '__main__':
    app.run(debug=True)
