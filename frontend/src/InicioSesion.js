import React, { useState } from "react";

function InicioSesion({ setToken }) {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append("usuario", usuario);
      formData.append("password", password);

      const response = await fetch("/Inicio", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setToken(data); // Suponiendo que el backend devuelve un token

        console.log("Inicio de sesión exitoso");
        setUsuario(data.usuario);
        setPassword("");
      } else {
        console.error("Error en el inicio de sesión");
      }
    } catch (error) {
      console.error("Error en el inicio de sesión:", error);
    }
  };

  return (
    <div>
      <h2>Inicio de Sesión</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="usuario">Usuario:</label>
          <input
            type="text"
            id="usuario"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
}

export default InicioSesion;
