import React, { useState, useEffect } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import sliderSettings from "../sliderSettings"; // Importa los ajustes

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
  const handleMarcarComoVisto = (titulo) => {
    if (!usuario) {
      alert("Por favor, selecciona un usuario primero.");
      return;
    }

    fetch(`/marcar_como_visto/${usuario}/${titulo}`, {
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

    fetch(`/marcar_quiere_ver/${usuario}/${titulo}`, {
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
      {Object.keys(data).map((genero, j) => {
        const moviesToShow = [...data[genero]];
        while (moviesToShow.length < 5) {
          moviesToShow.push({ empty: true });
        }

        return (
          <div key={j}>
            <h2>Porque viste {genero}</h2>
            <Slider {...sliderSettings}>
              {moviesToShow.map((movie, i) => (
                <div key={i} className="movie">
                  {movie.empty ? (
                    <div className="empty-movie"></div>
                  ) : (
                    <>
                      <img src={movie.img} alt={movie.title} />
                      <div className="movie-title">
                        <h4>{movie.title} ({movie.año}) - Rating: {movie.rating}</h4>
                      </div>
                      <div className="buttons">
                        <button className="button" onClick={() => handleMarcarQuiereVer(movie.title)}>Quiero Ver</button>
                        <button className="button" onClick={() => handleMarcarComoVisto(movie.title)}>Ver</button>
                      </div>
                    </>
                  )}
                </div>
              ))}
            </Slider>
          </div>
        );
      })}
    </div>
  );
}

export default Recomendar_Por_Generos;
