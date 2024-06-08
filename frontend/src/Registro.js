import React, { useState } from 'react';

function RegistroUsuario() {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [contra, setContra] = useState('');
  const [edad, setEdad] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Construye los datos del nuevo usuario
      const formData = new FormData();
      formData.append('nombre', nombre);
      formData.append('email', email);
      formData.append('contra', contra);
      formData.append('edad', edad);

      // Realiza la solicitud POST al endpoint /registro
      await fetch('/registro', {
        method: 'POST',
        body: formData
      });

      console.log('Usuario registrado exitosamente');
      // Limpia los campos después del envío
      setNombre('');
      setEmail('');
      setContra('');
      setEdad('');
    } catch (error) {
      console.error('Error al registrar el usuario:', error);
    }
  };

  return (
    <div>
      <h2>Registro de Usuario</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="nombre">Nombre:</label>
          <input
            type="text"
            id="nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="edad">Edad:</label>
          <input
            type="text"
            id="edad"
            value={edad}
            onChange={(e) => setEdad(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="contra">Contraseña:</label>
          <input
            type="password"
            id="contra"
            value={contra}
            onChange={(e) => setContra(e.target.value)}
            required
          />
        </div>
        <button type="submit">Registrarse</button>
      </form>
    </div>
  );
}

export default RegistroUsuario;
