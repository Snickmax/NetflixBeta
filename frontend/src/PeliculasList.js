// PeliculasList.js

import React, { useState, useEffect } from 'react';

function PeliculasList({ usuario }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/peliculas")
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
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return;
  }
  const handleMarcarComoVisto = (titulo) => {
    if (!usuario) {
      alert("Por favor, selecciona un usuario primero.");
      return;
    }

    fetch(`/marcar_como_visto/${usuario.nombre}/${titulo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          alert(`La película "${titulo}" ha sido marcada como vista.`);
        } else {
          alert(`No se pudo marcar la película "${titulo}" como vista.`);
        }
      })
      .catch(error => {
        alert(`Error: ${error.message}`);
      });
  };

  const handleMarcarQuiereVer = (titulo) => {
    if (!usuario) {
      alert("Por favor, selecciona un usuario primero.");
      return;
    }

    fetch(`/marcar_quiere_ver/${usuario.nombre}/${titulo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => res.json())
      .then(response => {
        if (response.success) {
          alert(`La película "${titulo}" ha sido agregada a tu lista.`);
        } else {
          alert(`No se pudo agregar la película "${titulo}" a tu lista.`);
        }
      })
      .catch(error => {
        alert(`Error: ${error.message}`);
      });
  };

  return (
    <div>
      <h2>Cartelera Completa</h2>
      <div className="cartelera">
      {data.map((movie, i) => (
          <div key={i} className="movie">
            {movie.empty ? (
              <div className="empty-movie"></div>
            ) : (
              <>
                <img src={movie.img} alt={movie.title} />
                <div className="movie-title">
                  <h3>
                    {movie.title} {movie.año} ({movie.rating})
                  </h3>
                </div>
                <div className="buttons">
                  <button className="button" onClick={() => handleMarcarComoVisto(movie.title)}>Ver</button>
                  <button className="button" onClick={() => handleMarcarQuiereVer(movie.title)}>Quiero Ver</button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PeliculasList;
