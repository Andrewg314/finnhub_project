import React from 'react'
import './HomePage.css'
import { useNavigate } from 'react-router'
import { useState, useEffect } from 'react'
import axios from 'axios'

const HomePage = () => {
  const [quotes, setQuotes] = useState([])
  const navigate = useNavigate();

  const keyLabels = {
    symbol: "Symbol",
    price: "Current price",
    change: "Change",
    percent_change: "Percent change",
    high_price: "High price of the day",
    low_price: "Low price of the day",
    open_price: "Open price of the day",
    prev_close_price: "Previous close price",
    timestamp_unix: "Published time"
  }

  const formatTimestamp = (ts) => {
    const date = new Date(ts * 1000)
    return date.toLocaleString()
  }

  const printAttributes = () => {
    return quotes.map((quote) => (
      <div key={quote.id}>
        <h3>{quote.symbol}</h3>
        <div><strong>{keyLabels.price}:</strong> {quote.price}</div>
        <div><strong>{keyLabels.change}:</strong> {quote.change}</div>
        <div><strong>{keyLabels.percent_change}:</strong> {quote.percent_change}%</div>
        <div><strong>{keyLabels.high_price}:</strong> {quote.high_price}</div>
        <div><strong>{keyLabels.low_price}:</strong> {quote.low_price}</div>
        <div><strong>{keyLabels.open_price}:</strong> {quote.open_price}</div>
        <div><strong>{keyLabels.prev_close_price}:</strong> {quote.prev_close_price}</div>
        <div><strong>{keyLabels.timestamp_unix}:</strong> {formatTimestamp(quote.timestamp_unix)}</div>
      </div>
    ))
  }

  const fetchAPI = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/quotes")
      setQuotes(response.data)
    } catch (error) {
      console.error("Error fetching quotes:", error)
    }
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <div>
      <h2>Stock Quotes</h2>
      {printAttributes()}

        <button onClick={() => navigate("/chart")}>
            Chart
        </button>
    </div>
  )
}

export default HomePage