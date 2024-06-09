import React from 'react';
import MasVistas from './Cartelera/MasVistas';
import NuevosLanzamientos from './Cartelera/NuevosLanzamientos';
import Peliculas_Vistas from './Cartelera/Peliculas_Vistas';
import Peliculas_Quiere_Ver from './Cartelera/Peliculas_Quiere_Ver';
import Peliculas_Calificadas from './Cartelera/Peliculas_Calificadas';

function App({ usuario }) {
  return (
    <div>
      <header>
        <h1>Bienvenido a nuestra Página de Recomendaciones</h1>
      </header>
      <main>
        <p>Aquí encontrarás recomendaciones personalizadas de películas.</p>

        <Peliculas_Vistas usuario={usuario.nombre} />
        <Peliculas_Quiere_Ver usuario={usuario.nombre} />
        <Peliculas_Calificadas usuario={usuario.nombre} />
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
