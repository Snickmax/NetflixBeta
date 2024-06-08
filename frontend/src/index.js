import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Registro from './Registro';
import './Style.css';


function Main() {
  const [showApp, setShowApp] = React.useState(true);

  return (
    <div>
      {showApp ? <Registro /> : <App />}
      <button onClick={() => setShowApp(!showApp)}>Cambiar a {showApp ? 'App' : 'Form'}</button>
    </div>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <Main />
  </React.StrictMode>,
  document.getElementById('root')
);
