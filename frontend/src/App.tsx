import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import RequirementForm from './pages/RequirementForm'
import RequirementDetail from './pages/RequirementDetail'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/requirement/new" element={
            <ProtectedRoute>
              <RequirementForm />
            </ProtectedRoute>
          } />
          <Route path="/requirement/:id" element={
            <ProtectedRoute>
              <RequirementDetail />
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </AuthProvider>
  )
}

export default App 