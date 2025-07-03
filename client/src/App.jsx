import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [quotes, setQuotes] = useState({
    c: 0,
    d: 0,
    dp: 0,
    h: 0,
    l: 0,
    o: 0,
    pc: 0,
    t: 0
  })

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:5000/api/quotes")
    setQuotes(response.data.AMD)
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <div>
      AMD:
      {quotes.c}
    </div>
  )
}

export default App
