import React, { useState, useEffect } from 'react';

function Recomendar_Por_Generos({ usuario }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/recomendarporgeneros/${usuario}`)
      .then(res => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, [usuario]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return;
  }

  return (
    <div>
      {Object.keys(data).map((genero, j) => (
            <div key={j}>
            <h3>Porque viste {genero}</h3>
            <div className="cartelera">
              {data[genero].map((movie, i) => (
              <div key={i} className="movie">
                <h4>{movie.title} ({movie.año}) - Rating: {movie.rating}</h4>
                <img src={movie.img} alt={movie.title} style={{ width: '200px', height: '300px' }} />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Recomendar_Por_Generos;
