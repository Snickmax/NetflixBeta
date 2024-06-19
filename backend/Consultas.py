# Crear una instancia de Driver para interactuar con la base de datos Neo4j
#   --- Consultas movies---
# mandamos los nuevos lanzamientos
def get_movie_nuevos_lanzamientos(tx, usuario):
    query = """
    MATCH (m:Pelicula)
    WHERE NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    ORDER BY año DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]

# mandamos las mas vistas
def get_movie_mas_vistas(tx, usuario):
    query = """
    MATCH (m:Pelicula)
    WHERE NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    }
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]

# mandamos las peliculas que quiere ver
def get_peliculas_quiere_ver(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]

#   --- Recomendacion de peliculas segun una que vio tanto recomendacion por la pelicula y generos ---
# peliculas que ya vio
def get_peliculas_vistas(tx, usuario):
    query = """
    MATCH (u:Usuario {nombre: $usuario})-[:VIO]->(m:Pelicula)
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]

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
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos=generos)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]

# Peliculas de generos independientes
def recomendar_peliculas_generos_independientes(tx, usuario, generos, pelis):
    query = """
    MATCH (m:Pelicula)-[:ES_DE]->(g:Genero)
    WHERE g.nombre IN $generos AND NOT EXISTS {
        MATCH (:Usuario {nombre: $usuario})-[:VIO]->(m)
    } AND NOT (m.titulo IN $pelis)
    RETURN DISTINCT m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    ORDER BY rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos=generos, pelis=pelis)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]
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
    RETURN m.titulo AS title, m.calificacion_promedio AS rating, m.año AS año, m.caratula AS img, COALESCE(peso, 0) AS peso,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    ORDER BY peso DESC, rating DESC
    LIMIT 10
    """
    result = tx.run(query, usuario=usuario, generos_mas_vistos=generos_mas_vistos)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "peso": record["peso"], "quiere_ver": record["quiere_ver"]} for record in result]

# Consulta para obtener todos los usuarios
def get_all_users(tx):
    query = """
    MATCH (u:Usuario)
    RETURN u.nombre AS nombre
    """
    result = tx.run(query)
    return [{"nombre": record["nombre"]} for record in result]

# Consulta para obtener todos los usuarios
def get_all_movies(tx, usuario):
    query = """
    MATCH (m:Pelicula)
    RETURN m.titulo AS title, m.año AS año, m.calificacion_promedio AS rating, m.caratula as img,
           EXISTS((:Usuario {nombre: $usuario})-[:QUIERE_VER]->(m)) AS quiere_ver
    """
    result = tx.run(query, usuario=usuario)
    return [{"title": record["title"], "rating": record["rating"], "año": record["año"], "img": record["img"], "quiere_ver": record["quiere_ver"]} for record in result]
#   --- Login ---
def verificar_usuario(tx, usuario, password):
    
    query = """
    MATCH (u:Usuario {nombre: $usuario, passd: $password})
    RETURN u.nombre AS nombre, u.passd AS password
    """
    result = tx.run(query, usuario=usuario, password=password)
    record = result.single()
    return record

def create_usuario(tx, hnombre_usuario, hedad, hemail, hfecha_registro, hpass):
    tx.run("MERGE (u:Usuario {nombre: $nombre, edad: $edad, email: $email, fecha_registro: $fecha_registro, passd: $passd})",
           nombre=hnombre_usuario, edad=hedad, email=hemail, fecha_registro=hfecha_registro, passd=hpass)

# CRUD Peliculas
def create_quiere_ver(tx, nombre_usuario, titulo_pelicula):
    query = """
    MATCH (u:Usuario {nombre: $nombre_usuario}), (p:Pelicula {titulo: $titulo_pelicula})
    MERGE (u)-[:QUIERE_VER]->(p)
    """
    tx.run(query, nombre_usuario=nombre_usuario, titulo_pelicula=titulo_pelicula)

def eliminar_quiere_ver(tx, nombre_usuario, titulo_pelicula):
    query = """
    MATCH (u:Usuario {nombre: $nombre_usuario})-[rel:QUIERE_VER]->(p:Pelicula {titulo: $titulo_pelicula})
    DELETE rel
    """
    tx.run(query, nombre_usuario=nombre_usuario, titulo_pelicula=titulo_pelicula)

def create_visto(tx, nombre_usuario, titulo_pelicula):
    query = """
    MATCH (u:Usuario {nombre: $nombre_usuario}), (p:Pelicula {titulo: $titulo_pelicula})
    MERGE (u)-[:VIO]->(p)
    """
    tx.run(query, nombre_usuario=nombre_usuario, titulo_pelicula=titulo_pelicula)