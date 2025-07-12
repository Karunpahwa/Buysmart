import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { LogOut, Home, Plus, Search } from 'lucide-react'

const Navigation: React.FC = () => {
  const { user, logout } = useAuth()
  const location = useLocation()

  const handleLogout = () => {
    logout()
  }

  const isActive = (path: string) => {
    return location.pathname === path
  }

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">BuySmart Assistant</h1>
            </Link>
            
            <nav className="hidden md:flex space-x-6">
              <Link
                to="/"
                className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/') 
                    ? 'bg-primary-100 text-primary-700' 
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Home className="h-4 w-4 mr-2" />
                Dashboard
              </Link>
              
              <Link
                to="/requirement/new"
                className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/requirement/new') 
                    ? 'bg-primary-100 text-primary-700' 
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Plus className="h-4 w-4 mr-2" />
                New Requirement
              </Link>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-2">
              <span className="text-sm text-gray-700">Welcome, {user?.email}</span>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              <LogOut className="h-4 w-4 mr-1" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Navigation 