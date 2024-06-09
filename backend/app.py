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

def get_users(tx):
    query = """
    MATCH (u:Usuario)
    RETURN u.nombre AS nombre
    """
    result = tx.run(query)
    return [{"nombre": record["nombre"]} for record in result]

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

def get_peliculas_vistas(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:VIO]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.caratula as img
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "img": record["img"]} for record in result]

def get_peliculas_quiere_ver(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.caratula as img
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "img": record["img"]} for record in result]

def get_peliculas_calificadas(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[r:CALIFICO]->(m:Pelicula)
    RETURN m.titulo AS title, r.rating AS rating, m.caratula as img
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "img": record["img"]} for record in result]

def create_usuario(tx, hnombre_usuario, hedad, hemail, hfecha_registro, hpass):
    tx.run("MERGE (u:Usuario {nombre: $nombre, edad: $edad, email: $email, fecha_registro: $fecha_registro, passd: $passd})",
           nombre=hnombre_usuario, edad=hedad, email=hemail, fecha_registro=hfecha_registro, passd=hpass)

def mostrar_todas_peliculas(tx):
    query = """
    MATCH (m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img, m.genero as gender
    ORDER BY title ASC
    """
    result = tx.run(query)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "genero": record["gender"]} for record in result]

@app.route('/usuarios', methods=['GET'])
def usuarios():
    try:
        with driver.session() as session:
            users = session.read_transaction(get_users)
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/peliculasVistas/<usuario>', methods=['GET'])
def get_peliculas_vistas(usuario):
    def query(tx, usuario):
        result = tx.run("MATCH (u:Usuario {nombre: $nombre})-[:VIO]->(p:Pelicula) RETURN p", nombre=usuario)
        return [record['p'] for record in result]
    
    with driver.session() as session:
        peliculas = session.execute_read(query, usuario)
        peliculas_list = [{'title': p['titulo'], 'fecha': p['año'], 'rating': p['calificacion_promedio'], 'img': p['caratula']} for p in peliculas]
    return jsonify(peliculas_list)


@app.route('/peliculasQuiereVer/<usuario>', methods=['GET'])
def get_peliculas_quiere_ver(usuario):
    def query(tx, usuario):
        result = tx.run("MATCH (u:Usuario {nombre: $nombre})-[:QUIERE_VER]->(p:Pelicula) RETURN p", nombre=usuario)
        return [record['p'] for record in result]
    
    with driver.session() as session:
        peliculas = session.execute_read(query, usuario)
        peliculas_list = [{'title': p['titulo'], 'fecha': p['año'], 'rating': p['calificacion_promedio'], 'img': p['caratula']} for p in peliculas]
    return jsonify(peliculas_list)

@app.route('/peliculasCalificadas/<usuario>', methods=['GET'])
def get_peliculas_calificadas(usuario):
    def query(tx, usuario):
        result = tx.run("MATCH (u:Usuario {nombre: $nombre})-[:CALIFICO]->(p:Pelicula) RETURN p", nombre=usuario)
        return [record['p'] for record in result]
    
    with driver.session() as session:
        peliculas = session.execute_read(query, usuario)
        peliculas_list = [{'title': p['titulo'], 'fecha': p['año'], 'rating': p['calificacion_promedio'], 'img': p['caratula']} for p in peliculas]
    return jsonify(peliculas_list)
    
@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    edad = request.form['edad']
    
    try:
        with driver.session() as session:
            session.write_transaction(create_usuario, nombre, edad, email, "2024-05-20", password)
        return jsonify({"message": "Usuario registrado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
    
@app.route('/peliculas')
def todas_peliculas():
    try:
        with driver.session() as session:
            results = session.read_transaction(mostrar_todas_peliculas)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
