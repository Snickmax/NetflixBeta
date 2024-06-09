import React, { useState, useEffect } from 'react';

function PeliculasQuiereVer({ usuario }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/peliculasQuiereVer/${usuario}`)
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
    return <p>Error: {error.message}</p>;
  }

  return (
    <div>
      <h2>Películas que {usuario} Quiere Ver</h2>
      <div className="cartelera">
        {data.map((movie, i) => (
          <div key={i} className="movie">
            <h3>{movie.title} ({movie.fecha})</h3>
            <img src={movie.img} alt={movie.title} style={{ width: '200px', height: '300px' }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default PeliculasQuiereVer;
