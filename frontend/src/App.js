import React, { useState, useEffect } from 'react';
import MasVistas from './Cartelera/MasVistas';
import NuevosLanzamientos from './Cartelera/NuevosLanzamientos';


function App() {
  return (
    <div>
      <header>
        <a href = "Form.js">Inicio</a>
      </header>
      <main>
        <h1>Bienvenido a nuestra Página de Recomendaciones</h1>
        <p>Aquí encontrarás recomendaciones personalizadas de películas.</p>
        
        <MasVistas/>
        <NuevosLanzamientos/>

      </main>
      <footer>
        <p>© 2024 Mi Sitio de Recomendaciones</p>
      </footer>
    </div>
  );
}

export default App;