from flask import Flask, jsonify, request
from flask_cors import CORS
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import jwt
import datetime
from Consultas import *

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app)

# Configurar la conexión a la base de datos Neo4j
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "papupro")

# Crear una instancia de Driver para interactuar con la base de datos Neo4j
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

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
                token = jwt.encode({
                    'sub': usuario,
                    'iat': datetime.datetime.utcnow(),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, SECRET_KEY, algorithm='HS256')
                
                return jsonify({"token": token, "usuario": usuario})
            else:
                return jsonify({"error": "Credenciales inválidas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cerrar_sesion', methods=['POST'])
def logout():
    # In a real scenario, you might blacklist the token
    return jsonify({"message": "Sesión cerrada exitosamente"})

#   --- recomendaciones ---

"""
nuevos_lanzamientos():
    Función: Esta ruta devuelve las últimas películas lanzadas que el usuario aún no ha visto.
    
    Respuesta: Devuelve una lista de hasta 10 películas ordenadas por año de lanzamiento, con su título, calificación promedio, año y carátula.
"""
@app.route('/nuevoslanzamientos/<usuario>', methods=['GET'])
def nuevos_lanzamientos(usuario):

    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_nuevos_lanzamientos, usuario)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# peliculas vistas
@app.route('/peliculasvistas/<usuario>', methods=['GET'])
def peliculas_vistas(usuario):
    if not usuario:
        return jsonify({"error": "Usuario no proporcionado"}), 400

    try:
        with driver.session() as session:
            results = session.read_transaction(get_peliculas_vistas, usuario)
        
        if not results:
                return jsonify({"error": "No se encontraron peliculas para el usuario proporcionado"}), 404
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# peliculas quiere ver
@app.route('/quierever/<usuario>', methods=['GET'])
def peliculas_quiere_ver(usuario):
    if not usuario:
        return jsonify({"error": "Usuario no proporcionado"}), 400

    try:
        with driver.session() as session:
            results = session.read_transaction(get_peliculas_quiere_ver, usuario)
        
        if not results:
                return jsonify({"error": "No se encontraron peliculas para el usuario proporcionado"}), 404
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
mas_vistas():
    Función: Esta ruta devuelve las películas más vistas que el usuario aún no ha visto.
    Respuesta: Devuelve una lista de hasta 10 películas ordenadas por calificación promedio, con su título, calificación promedio, año y carátula.
"""
@app.route('/masvistas/<usuario>', methods=['GET'])
def mas_vistas(usuario):
    
    try:
        with driver.session() as session:
            results = session.read_transaction(get_movie_mas_vistas, usuario)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
recomendar_por_generos():
    Función: Esta ruta recomienda películas al usuario basadas en los géneros que más ha visto.
    Respuesta: Devuelve un diccionario donde las claves son los géneros más vistos por el usuario y los valores son listas de hasta 10 películas recomendadas por cada género. Cada película incluye su título, calificación promedio, año y carátula.
"""
@app.route('/recomendarporgeneros/<usuario>', methods=['GET'])
def recomendar_por_generos(usuario):
    if not usuario:
        return jsonify({"error": "Usuario no proporcionado"}), 400
    
    try:
        with driver.session() as session:
            generos_mas_vistos = session.read_transaction(get_generos_mas_vistos_por_usuario, usuario)
            if not generos_mas_vistos:
                return jsonify({"error": "No se encontraron géneros para el usuario proporcionado"}), 404
            
            recomendaciones = {}
            for genero in generos_mas_vistos:
                peliculas_recomendadas = session.read_transaction(recomendar_peliculas_generos_independientes, usuario, [genero],[])
                if peliculas_recomendadas:
                    recomendaciones[genero] = peliculas_recomendadas

            return jsonify(recomendaciones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
recomendar_por_pelicula():
    Función: Esta ruta recomienda películas al usuario basadas en una película específica que ha visto.
    Respuesta: Devuelve una lista de hasta 10 películas recomendadas. Incluye las películas del mismo género que la película proporcionada, seguidas de películas de géneros independientes. Cada película incluye su título, calificación promedio, año y carátula.
"""
@app.route('/recomendarporpelicula/<usuario>/<titulo>', methods=['GET'])
def recomendar_por_pelicula(usuario, titulo):
    if not usuario or not titulo:
        return jsonify({"error": "Usuario o título de película no proporcionado"}), 400
    
    try:
        with driver.session() as session:
            generos = session.read_transaction(get_generos_de_pelicula_vista, usuario, titulo)
            if not generos:
                return jsonify({"error": "No se encontraron géneros para la película proporcionada"}), 404

            mismas_generos_peliculas = session.read_transaction(recomendar_peliculas_mismos_generos, usuario, generos)
            pelis = [ peli['title'] for peli in mismas_generos_peliculas]

            combinadas_peliculas = mismas_generos_peliculas
            if len(mismas_generos_peliculas) < 10:
                generos_independientes_peliculas = session.read_transaction(recomendar_peliculas_generos_independientes, usuario, generos, pelis)
                combinadas_peliculas += generos_independientes_peliculas
                combinadas_peliculas = combinadas_peliculas[:10]  # Limitar a 10 resultados

            return jsonify(combinadas_peliculas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
recomendaciones_para_ti():
    Función: Esta ruta proporciona recomendaciones personalizadas al usuario basadas en sus géneros de películas más vistos.
    Respuesta: Devuelve una lista de hasta 10 películas recomendadas para el usuario. Las películas están seleccionadas en función de los géneros más vistos por el usuario. Cada película incluye su título, calificación promedio, año y carátula.
"""
@app.route('/recomendacionesparati/<usuario>', methods=['GET'])
def recomendaciones_para_ti(usuario):
    if not usuario:
        return jsonify({"error": "Usuario no proporcionado"}), 400
    
    try:
        with driver.session() as session:
            generos_mas_vistos = session.read_transaction(get_generos_mas_vistos_por_usuario2, usuario)
            if not generos_mas_vistos:
                return jsonify({"error": f"No se encontraron géneros para el usuario {usuario}"}), 404
            
            recomendaciones = session.read_transaction(get_recomendaciones_para_ti, usuario, generos_mas_vistos)

            return jsonify(recomendaciones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        with driver.session() as session:
            usuarios = session.read_transaction(get_all_users)
            return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Ruta para obtener todas las películas
@app.route('/peliculas/<usuario>', methods=['GET'])
def obtener_peliculas(usuario):
    if not usuario:
        return jsonify({"error": "Usuario o título de película no proporcionado"}), 400
    
    try:
        with driver.session() as session:
            peliculas = session.read_transaction(get_all_movies, usuario)
            return jsonify(peliculas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/marcar_como_visto/<usuario>/<titulo>', methods=['POST'])
def marcar_como_visto(usuario, titulo):

    if not usuario or not titulo:
        return jsonify({"success": False, "message": "Datos insuficientes."}), 400

    try:
        with driver.session() as session:
            session.write_transaction(create_visto, usuario, titulo)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@app.route('/marcar_quiere_ver/<usuario>/<titulo>', methods=['POST'])
def marcar_quiere_ver(usuario, titulo):

    if not usuario or not titulo:
        return jsonify({"success": False, "message": "Datos insuficientes."}), 400

    try:
        with driver.session() as session:
            session.write_transaction(create_quiere_ver, usuario, titulo)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/desmarcar_quiere_ver/<usuario>/<titulo>', methods=['POST'])
def desmarcar_quiere_ver(usuario, titulo):

    if not usuario or not titulo:
        return jsonify({"success": False, "message": "Datos insuficientes."}), 400

    try:
        with driver.session() as session:
            session.write_transaction(eliminar_quiere_ver, usuario, titulo)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
