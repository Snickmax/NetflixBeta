import React from 'react';
import MasVistas from './Cartelera/MasVistas';
import NuevosLanzamientos from './Cartelera/NuevosLanzamientos';
import Peliculas_Vistas from './Cartelera/Peliculas_Vistas';
import Peliculas_Quiere_Ver from './Cartelera/Peliculas_Quiere_Ver';
import Peliculas_Para_Ti from './Cartelera/Peliculas_Para_Ti';
import Recomendar_Por_Generos from './Cartelera/Recomendar_Por_Generos';

function App({ usuario }) {
  return (
    <div>
      <header>
        <h1>Bienvenido a nuestra Página de Recomendaciones</h1>
      </header>
      <main>
        <p>Aquí encontrarás recomendaciones personalizadas de películas.</p>

        <MasVistas />
        <NuevosLanzamientos />
        <Peliculas_Vistas usuario={usuario.nombre} />
        <Peliculas_Quiere_Ver usuario={usuario.nombre} />
        <Peliculas_Para_Ti usuario={usuario.nombre} />
        <Recomendar_Por_Generos usuario={usuario.nombre} />
        
        
      </main>
      <footer>
        <p>© 2024 Mi Sitio de Recomendaciones</p>
      </footer>
    </div>
  );
}

export default App;
