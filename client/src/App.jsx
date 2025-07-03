import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [quotes, setQuotes] = useState([])

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:5000/api/quotes")
    setQuotes(response.data.users)
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <div>
      hi
      {quotes}
    </div>
  )
}

export default App
