import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import RequirementForm from './pages/RequirementForm'
import RequirementDetail from './pages/RequirementDetail'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/requirement/new" element={<RequirementForm />} />
        <Route path="/requirement/:id" element={<RequirementDetail />} />
      </Routes>
    </div>
  )
}

export default App 