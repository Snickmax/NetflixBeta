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

def get_movie_nuevos_lanzamientos(tx):
    query = """
    MATCH (m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY año DESC
    LIMIT 10
    """
    result = tx.run(query)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]

def get_movie_mas_vistas(tx):
    query = """
    MATCH (m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]
    
# Ruta para obtener recomendaciones de películas
@app.route('/nuevoslanzamientos')
def recommendations():
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_nuevos_lanzamientos)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/masvistas')
def nuevos_lanzamientos():
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_mas_vistas)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_usuario(tx, hnombre_usuario, hedad, hemail, hfecha_registro, hpass):
    tx.run("MERGE (u:Usuario {nombre: $nombre, edad: $edad, email: $email, fecha_registro: $fecha_registro, passd: $passd})",
           nombre=hnombre_usuario, edad=hedad, email=hemail, fecha_registro=hfecha_registro, passd=hpass)


@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    edad = request.form['edad']
    
    try:
        with driver.session() as session:
            session.write_transaction(create_usuario, nombre, edad, email,"2024-05-20",password)
        return jsonify({"message": "Usuario registrado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
