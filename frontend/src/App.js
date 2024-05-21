import React, { useState, useEffect } from 'react'

function App() {

  const [data,  setData] = useState([{}])

  useEffect(() => {
    fetch("/recommendations").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )

  }, [])

  return (
    <div>
      {(typeof data.cartelera === "undefined") ? (
        <p>Loading...</p>
      ) : (
        data.cartelera.map((movie, i) =>(
          <p key={i}> {movie.title} {movie.rating}</p>
        )

        )
      )
      
      }
    </div>
  )
}

export default App