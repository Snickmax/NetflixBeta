import React, { useState, useEffect } from "react";
import Recomendacion_Por_Titulo from "./Recomendacion_Por_Titulo";

function Rec_Peli({ usuario }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const MAX_RANDOM_MOVIES = 5;

  useEffect(() => {
    if (usuario) {
      fetch(`/peliculasvistas/${usuario}`)
        .then((res) => {
          if (!res.ok) {
            throw new Error("Network response was not ok");
          }
          return res.json();
        })
        .then((data) => {
          setData(data);
          setLoading(false);
        })
        .catch((error) => {
          setError(error);
          setLoading(false);
        });
    } else {
      // Si el usuario es null, establece los datos como vacíos y detiene la carga
      setData([]);
      setLoading(true);
    }
  }, [usuario]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return;
  }

  // Calcula el número máximo de películas aleatorias
  const numMovies = data.length;
  const maxRandomMovies = Math.min(numMovies, MAX_RANDOM_MOVIES);

  // Obtiene películas aleatorias
  const randomMovies = data
    .sort(() => Math.random() - 0.5)
    .slice(0, maxRandomMovies);

  return (
    <div>
      {randomMovies.map((movie, i) => (
        <Recomendacion_Por_Titulo
          key={i}
          usuario={usuario}
          titulo={movie.title}
        />
      ))}
    </div>
  );
}

export default Rec_Peli;
