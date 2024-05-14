from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Modtag data fra formular
        hold_navn = request.form['hold_navn']
        antal_maal = request.form['antal_maal']

        # Opret forbindelse til databasen
        conn = sqlite3.connect('fodbold_turnering.db')
        cur = conn.cursor()

        # Indsæt data i databasen
        cur.execute("INSERT INTO hold (hold_navn, point) VALUES (?, ?)", (hold_navn, antal_maal))

        # Gem ændringer
        conn.commit()

        # Luk forbindelsen til databasen
        conn.close()

        # Omdiriger tilbage til hjemmesiden
        return redirect('/')

    else:
        # Opret forbindelse til databasen
        conn = sqlite3.connect('fodbold_turnering.db')
        cur = conn.cursor()

        # Hent hold og point fra databasen
        cur.execute("SELECT hold_navn, point FROM hold")
        hold = cur.fetchall()

        # Luk forbindelsen til databasen
        conn.close()

        # Render HTML-skabelonen med hold og point
        return render_template('index.html', hold=hold)

if __name__ == '__main__':
    app.run(debug=True)
