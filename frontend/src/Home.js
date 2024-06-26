import React from "react";
import MasVistas from "./Cartelera/MasVistas";
import NuevosLanzamientos from "./Cartelera/NuevosLanzamientos";
import Peliculas_Vistas from "./Cartelera/Peliculas_Vistas";
import Peliculas_Quiere_Ver from "./Cartelera/Peliculas_Quiere_Ver";
import Peliculas_Para_Ti from "./Cartelera/Peliculas_Para_Ti";
import Recomendar_Por_Generos from "./Cartelera/Recomendar_Por_Generos";
import Rec_Peli from "./Cartelera/Rec_Peli";

function Home({ usuario }) {
  return (
    <main>
      <p>Aquí encontrarás recomendaciones personalizadas de películas.</p>

      <Peliculas_Vistas usuario={usuario} />
      <Peliculas_Quiere_Ver usuario={usuario} />
      <Peliculas_Para_Ti usuario={usuario} />
      <MasVistas usuario={usuario} />
      <NuevosLanzamientos usuario={usuario} />
      <Recomendar_Por_Generos usuario={usuario} />
      <Rec_Peli usuario={usuario} />
    </main>
  );
}

export default Home;
