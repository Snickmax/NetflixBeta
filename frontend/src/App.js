import React, { useState, useEffect } from "react";
import RegistroUsuario from "./RegistroUsuario";
import InicioSesion from "./InicioSesion";
import Home from "./Home";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [usuario, setUsuario] = useState(null);

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
          <Home usuario={usuario} handleLogout={handleLogout} />
        </>
      )}
    </div>
  );
}

export default App;
