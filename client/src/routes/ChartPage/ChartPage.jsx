import React from 'react'
import { useNavigate } from 'react-router'

const ChartPage = () => {
  const navigate = useNavigate();
    return (
    <div>
        <h2>ChartPage</h2>

        <button onClick={() => navigate("/")}>
        Home
        </button>
    </div>
  )
}

export default ChartPage