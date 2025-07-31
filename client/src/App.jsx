import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router'
import HomePage from './routes/HomePage/HomePage'
import ChartPage from './routes/ChartPage/ChartPage'

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />}/>
          <Route path="/chart" element={<ChartPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App