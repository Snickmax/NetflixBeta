import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Registro from './Registro';
import PeliculasList from './PeliculasList'; 
import './Style.css';

function Main() {
  const [usuarios, setUsuarios] = useState([]);
  const [selectedUsuario, setSelectedUsuario] = useState(null);
  const [mostrarRegistro, setMostrarRegistro] = useState(false);
  const [mostrarPeliculas, setMostrarPeliculas] = useState(false); // Estado para mostrar las películas


  useEffect(() => {
    const fetchUsuarios = async () => {
      const response = await fetch('/usuarios');
      const data = await response.json();
      setUsuarios(data);
    };
    fetchUsuarios();
  }, []);

  const handleUsuarioChange = (e) => {
    const usuarioNombre = e.target.value;
    const usuario = usuarios.find(u => u.nombre === usuarioNombre);
    setSelectedUsuario(usuario);
  };

  const handleRegistroClick = () => {
    setMostrarRegistro(true);
  };

  const handleMostrarPeliculasClick = () => {
    setMostrarPeliculas(true);
    setMostrarRegistro(false);
  };

  const handleVolverInicioClick = () => {
    setMostrarPeliculas(false);
    setMostrarRegistro(false);
  };

  const handleRegistroSuccess = () => {
    setMostrarRegistro(false);
    const fetchUsuarios = async () => {
      const response = await fetch('/usuarios');
      const data = await response.json();
      setUsuarios(data);
    };
    fetchUsuarios();
  };

  return (
    <div>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <button onClick={handleRegistroClick} style={{ marginRight: '20px' }}>Registrarse</button>
          <button onClick={handleVolverInicioClick} style={{ marginRight: '20px' }}>Volver al Inicio</button>
          <button onClick={handleMostrarPeliculasClick} style={{ marginRight: '20px' }}>Mostrar películas</button> {/* Botón para mostrar las películas */}
          <select id="selectUsuario" onChange={handleUsuarioChange} value={selectedUsuario ? selectedUsuario.nombre : ""}>
            <option value="" disabled>Selecciona un usuario</option>
            {usuarios.map((usuario, index) => (
              <option key={index} value={usuario.nombre}>
                {usuario.nombre}
              </option>
            ))}
          </select>
        </div>
      </header>
      <main>
        {mostrarRegistro ? (
          <Registro onRegistroSuccess={handleRegistroSuccess} />
        ) : mostrarPeliculas ? (
          <PeliculasList /> // Mostramos PeliculasList cuando se hace clic en "Mostrar películas"
        ) : (
          selectedUsuario ? (
            <App usuario={selectedUsuario} />
          ) : (
            <p>Por favor, selecciona un usuario para ver sus películas.</p>
          )
        )}
      </main>
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <Main />
  </React.StrictMode>,
  document.getElementById('root')
);
