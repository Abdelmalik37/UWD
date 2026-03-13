import { NavLink, Route, Routes } from 'react-router-dom'

import DashboardPage from './pages/DashboardPage'
import HistoryPage from './pages/HistoryPage'
import UploadPage from './pages/UploadPage'

export default function App() {
  return (
    <div className="layout">
      <header className="topbar">
        <h1>UWD Wearable Converter</h1>
        <nav>
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/upload">Upload Data</NavLink>
          <NavLink to="/history">Upload History</NavLink>
        </nav>
      </header>

      <main className="content">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </main>
    </div>
  )
}
