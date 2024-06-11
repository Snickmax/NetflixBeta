import React, { useState, useEffect } from "react";
import RegistroUsuario from "./RegistroUsuario";
import InicioSesion from "./InicioSesion";
import Home from "./Home";
import PeliculasList from "./PeliculasList";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [usuario, setUsuario] = useState(null);
  const [mostrarPeliculas, setMostrarPeliculas] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUsuario = localStorage.getItem("usuario");
    if (storedToken) {
      setToken(storedToken);
    }
    if (storedUsuario) {
      setUsuario(storedUsuario);
    }
  }, []);

  const handleMostrarPeliculasClick = () => {
    setMostrarPeliculas(true);
  };

  const handleVolverInicioClick = () => {
    setMostrarPeliculas(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    setToken(null);
    setUsuario(null);
  };

  const handleLogin = (data) => {
    localStorage.setItem("token", data.token);
    localStorage.setItem("usuario", data.usuario);
    setToken(data.token);
    setUsuario(data.usuario);
  };

  return (
    <div>
      {!token ? (
        <>
          <RegistroUsuario />
          <InicioSesion setToken={handleLogin} />
        </>
      ) : (
        <>
        <header>
        <h1>Bienvenido {usuario} a nuestra Página de Recomendaciones</h1>
        <button onClick={handleLogout}>Cerrar Sesión</button>
        {mostrarPeliculas ? (
          <button onClick={handleVolverInicioClick}>HOME</button>
        ) : (
          <button onClick={handleMostrarPeliculasClick}>Cartelera</button>
        )}
      </header>
          {mostrarPeliculas ? (
            <PeliculasList
              usuario={usuario}
            />
          ) : (
            <Home
              usuario={usuario}
            />
          )}
        </>
      )}
      <footer>
        <p>© 2024 Mi Sitio de Recomendaciones</p>
      </footer>
    </div>
  );
}

export default App;
