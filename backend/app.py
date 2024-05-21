from flask import Flask

app = Flask(__name__)

# Ruta para obtener recomendaciones de películas
@app.route('/recommendations')
def get_recommendations():
    # Lógica para obtener recomendaciones de películas del usuario con el ID proporcionado
    # Aquí puedes ejecutar consultas en la base de datos Neo4j y procesar los resultados
    return { "cartelera": [ {"title": "Movie 1", "rating": 4.5} ,
        {"title": "Movie 2", "rating": 4.0},
        {"title": "Movie 3", "rating": 3.5}]
        }

if __name__ == '__main__':
    app.run(debug=True)
