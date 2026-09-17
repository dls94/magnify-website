import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Header from './components/layout/Header/Header'
import './components/layout/Header/Header.css'
import Artists from './pages/Artists/Artists'
import Events from './pages/Events/Events'
import Home from './pages/Home/Home'
import Releases from './pages/Releases/Releases'

function App() {
  return (
    <BrowserRouter>
      <Header />

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/artists" element={<Artists />} />
          <Route path="/releases" element={<Releases />} />
          <Route path="/events" element={<Events />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App