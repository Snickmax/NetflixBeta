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

#   --- Consultas movies---
# mandamos los nuevos lanzamientos
def get_movie_nuevos_lanzamientos(tx, usuario):
    query = """
    MATCH (m:Pelicula)
    WHERE NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY año DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]

# mandamos las mas vistas
def get_movie_mas_vistas(tx, usuario):
    query = """
    MATCH (m:Pelicula)
    WHERE NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]

# mandamos las peliculas que quiere ver
def get_peliculas_quiere_ver(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.caratula as img
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "img": record["img"]} for record in result]

#   --- Recomendacion de peliculas segun una que vio tanto recomendacion por la pelicula y generos ---
# peliculas que ya vio
def get_peliculas_vistas(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:VIO]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.caratula as img
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "img": record["img"]} for record in result]

# genero de las pelicula vista
def get_generos_de_pelicula_vista(tx, usuario, titulo):
    query = """
    MATCH (:Usuario {nombre: $usuario})-[:VIO]->(p:Pelicula {titulo: $titulo})-[:ES_DE]->(g:Genero)
    RETURN g.nombre AS genero
    """
    result = tx.run(query, usuario=usuario, titulo=titulo)
    return [record["genero"] for record in result]

# Peliculas de los mismos generos mas de 1
def recomendar_peliculas_mismos_generos(tx, usuario, generos):
    query = """
    MATCH (m:Pelicula)-[:ES_DE]->(g:Genero)
    WHERE g.nombre IN $generos AND NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    WITH m, COLLECT(g.nombre) AS movieGenres
    WHERE ALL(genre IN $generos WHERE genre IN movieGenres) AND SIZE(movieGenres) = SIZE($generos)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos=generos)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]

# Peliculas de generos independientes
def recomendar_peliculas_generos_independientes(tx, usuario, generos):
    query = """
    MATCH (m:Pelicula)-[:ES_DE]->(g:Genero)
    WHERE g.nombre IN $generos AND NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    RETURN DISTINCT m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos=generos)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"]} for record in result]

# Peliculas de generos independientes
def get_generos_mas_vistos_por_usuario(tx, usuario):
    query = """
    MATCH (:Usuario {nombre: $usuario})-[:VIO]->(:Pelicula)-[:ES_DE]->(g:Genero)
    RETURN g.nombre AS genero, COUNT(*) AS count
    ORDER BY count DESC
    """
    result = tx.run(query, usuario=usuario)
    return [record["genero"] for record in result]

def get_generos_mas_vistos_por_usuario2(tx, usuario):
    query = """
    MATCH (:Usuario {nombre: $usuario})-[:VIO]->(:Pelicula)-[:ES_DE]->(g:Genero)
    RETURN g.nombre AS genero, COUNT(*) AS count
    ORDER BY count DESC
    """
    result = tx.run(query, usuario=usuario)
    return [{"genero": record["genero"], "count": record["count"]} for record in result]

def get_recomendaciones_para_ti(tx, usuario, generos_mas_vistos):
    query = """
    MATCH (m:Pelicula)
    WHERE NOT EXISTS { (:Usuario {nombre: $usuario})-[:VIO]->(m) }
    OPTIONAL MATCH (m)-[:ES_DE]->(g:Genero)
    WITH m, $generos_mas_vistos AS generos_mas_vistos, COLLECT(g.nombre) AS pelicula_generos
    WITH m, generos_mas_vistos, [gen IN generos_mas_vistos WHERE gen.genero IN pelicula_generos | gen.count] AS pesos
    WITH m, REDUCE(s = 0, p IN pesos | s + p) AS peso
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula AS img, COALESCE(peso, 0) AS peso
    ORDER BY peso DESC, rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos_mas_vistos=generos_mas_vistos)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "peso": record["peso"]} for record in result]

#   --- Login ---
def verificar_usuario(tx, usuario, password):
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

@app.route('/Inicio', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']
    
    try:
        with driver.session() as session:
            user = session.read_transaction(verificar_usuario, usuario, password)
            if user:
                peliculas_vistas = session.read_transaction(get_peliculas_vistas, usuario)
                peliculas_favoritas = session.read_transaction(get_peliculas_quiere_ver, usuario)
                return jsonify({
                    "usuario": {"nombre": user["nombre"], "password": user["password"]},
                    "peliculasVistas": peliculas_vistas,
                    "peliculasFavoritas": peliculas_favoritas
                })
            else:
                return jsonify({"error": "Credencdddiales inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevoslanzamientos')
def recommendations():
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_nuevos_lanzamientos, usuario)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
mas_vistas():
    Función: Esta ruta devuelve las películas más vistas que el usuario aún no ha visto.
    Respuesta: Devuelve una lista de hasta 10 películas ordenadas por calificación promedio, con su título, calificación promedio, año y carátula.
"""
@app.route('/masvistas', methods=['GET'])
def mas_vistas():
    usuario = request.args.get('usuario')
    if not usuario:
        return jsonify({"error": "Usuario no proporcionado"}), 400
    
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_mas_vistas, usuario)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
