from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'niggerz'
API = "https://pokeapi.co/api/v2/pokemon/"
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search_pokemon():
    pokemon = request.form.get('pokemon', '').strip().lower()

    if not pokemon:
        flash('Porfavor ingresa un nombre de un pokemon', 'error')
        return redirect(url_for('index'))
    
try:
        resp = requests.get(f"{API}{pokemon}")
        if resp.status_code == 200:
            pokemon_data = resp.json()
            return render_template('pokemon.html', pokemon=pokemon_data)
        else:
            flash(f'Pokemon "{pokemon}" no encontrado', 'error')
            return redirect(url_for('index'))
except requests.exceptions.RequestException as e:
    flash('Error al buscar el Pokemon', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 