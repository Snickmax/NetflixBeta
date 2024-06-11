// sliderSettings.js
const settings = {
  dots: true,
  infinite: false, // Desactiva el giro infinito
  speed: 500,
  slidesToShow: 5, // Muestra 5 elementos a la vez en pantallas grandes
  slidesToScroll: 5, // Se desplaza 5 elementos a la vez
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 4,
      },
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
      },
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
      },
    },
  ],
};

export default settings;
