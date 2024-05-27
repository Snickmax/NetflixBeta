from flask import Flask, jsonify, request
from flask_cors import CORS
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app)

# Configurar la conexión a la base de datos Neo4j
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Crear una instancia de Driver para interactuar con la base de datos Neo4j
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def get_movie_recommendations(tx, user_id):
    query = """
    MATCH (a:Actor {nombre: $user_id})-[r:ACTUÓ_EN]->(m:Pelicula)
    RETURN m.titulo AS title, m.rating AS rating
    LIMIT 25
    """
    result = tx.run(query, user_id=user_id)
    return [{"title": record["title"], "rating": record["rating"]} for record in result]

# Ruta para obtener recomendaciones de películas
@app.route('/recommendations')
def recommendations():
    user_id = "Tom Hanks"
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_recommendations, user_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
