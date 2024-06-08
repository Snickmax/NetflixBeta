import React from 'react';
import MasVistas from './Cartelera/MasVistas';
import NuevosLanzamientos from './Cartelera/NuevosLanzamientos';

function App({ usuario, peliculasVistas, peliculasFavoritas }) {
  return (
    <div>
      <header>
        <a href="Registro.js">Inicio</a>
      </header>
      <main>
        <h1>Bienvenido a nuestra Página de Recomendaciones</h1>
        <p>Aquí encontrarás recomendaciones personalizadas de películas.</p>
        
        <h2>Películas Vistas por {usuario.nombre}</h2>
        <div>
          {peliculasVistas.length > 0 ? peliculasVistas.map((pelicula, index) => (
            <div key={index}>
              <h3>{pelicula.title}</h3>
              <p>Rating: {pelicula.rating}</p>
              <img src={pelicula.img} alt={pelicula.title} />
            </div>
          )) : <p>No ha visto ninguna película aún.</p>}
        </div>

        <h2>Películas Favoritas de {usuario.nombre}</h2>
        <div>
          {peliculasFavoritas.length > 0 ? peliculasFavoritas.map((pelicula, index) => (
            <div key={index}>
              <h3>{pelicula.title}</h3>
              <p>Rating: {pelicula.rating}</p>
              <img src={pelicula.img} alt={pelicula.title} />
            </div>
          )) : <p>No tiene películas favoritas aún.</p>}
        </div>

        <MasVistas />
        <NuevosLanzamientos />

      </main>
      <footer>
        <p>© 2024 Mi Sitio de Recomendaciones</p>
      </footer>
    </div>
  );
}

export default App;
