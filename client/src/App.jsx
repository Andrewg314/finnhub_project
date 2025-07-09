import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'

function App() {
  const [quotes, setQuotes] = useState({})
  
  const keyLabels = {
    c: "Current price",
    d: "Change",
    dp: "Percent change",
    h: "High price of the day",
    l: "Low price of the day",
    o: "Open price of the day",
    pc: "Previous close price",
    t: "Published time in UNIX timestamp"
  }

  const printAttributes = () => {
  return Object.entries(quotes).map(([ticker, data]) => (
    <div key={ticker}>
      <strong>{ticker}</strong>
      {Object.entries(data).map(([key, value]) => (
        <div key={key}>
          <strong>{keyLabels[key] || key}</strong>: {value}
        </div>
      ))}
      <br />
    </div>
  ))
}

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:5000/api/quotes")
    setQuotes(response.data)
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <div>
      <h2>Stock Quotes</h2>
      {printAttributes()}
    </div>
  )
}

export default App
