from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'free_fire' # Esto es indispensable a la hora de trabajar con formularios
API = "https://pokeapi.co/api/v2/pokemon/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_pokemon():
    nombre_pokemon = request.form.get('nombre_pokemon', '').strip().lower()

    if not nombre_pokemon:
        flash('Porfavor ingresa un nombre de un pokemon', 'error')
        return redirect(url_for('index'))
    
    try: # Atrapa errores 
        resp = requests.get(f"{API}{nombre_pokemon}")
        if resp.status_code == 200:
            pokemon_data = resp.json()

            pokemon_info = { 
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': round(pokemon_data['height'] / 10, 1), # Convertir a metros
                'weight': round(pokemon_data['weight'] / 10, 1), # Convertir a kg
                'image': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']],
            }
            
            print(f"Debug - Altura: {pokemon_info['height']}, Peso: {pokemon_info['weight']}")

            return render_template('pokemon.html', 
                                 pokemon=pokemon_info, 
                                 nombre_pokemon=pokemon_info['name'])
        else:
            flash(f'Pokemon "{nombre_pokemon}" no encontrado', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('Error al buscar el Pokemon', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 